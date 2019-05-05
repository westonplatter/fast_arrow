import imaplib
import os
import random
import time
import re
import json
from datetime import datetime, timedelta

import requests
from fast_arrow.exceptions import AuthenticationError, NotImplementedError
from fast_arrow.resources.account import Account
from fast_arrow.resources.user import User
from fast_arrow.util import get_last_path

CLIENT_ID = "c82SH0WZOsabOXGP2sxqcj34FxkvfnWRZBKlBjFS"

HTTP_ATTEMPTS_MAX = 2


class Client(object):

    def __init__(self, **kwargs):
        self.options = kwargs
        self.account_id     = None
        self.account_url    = None
        self.access_token   = None
        self.refresh_token  = None
        self.mfa_code       = None
        self.device_token   = None
        self.scope          = None
        self.authenticated  = False
        self.certs = os.path.join(os.path.dirname(__file__), 'ssl_certs/certs.pem')


    def authenticate(self):
        '''
        Authenticate using data in `options`
        '''
        if "username" in self.options and "password" in self.options:
            self.login_oauth2(self.options["username"], self.options["password"], self.options.get('mfa_code'))
        elif "access_token" in self.options and "refresh_token" in self.options:
            self.access_token = self.options["access_token"]
            self.refresh_token = self.options["refresh_token"]
            self.__set_account_info()
        else:
            self.authenticated = False
        return self.authenticated


    def get(self, url=None, params=None, retry=True):
        '''
        Execute HTTP GET
        '''
        headers = self._gen_headers(self.access_token, url)
        attempts = 1
        while attempts <= HTTP_ATTEMPTS_MAX:
            try:
                res = requests.get(url, headers=headers, params=params, timeout=15, verify=self.certs)
                res.raise_for_status()
                return res.json()
            except requests.exceptions.RequestException as e:
                attempts += 1
                if res.status_code in [400]:
                    raise e
                elif retry and res.status_code in [403]:
                    self.relogin_oauth2()


    def post(self, url=None, payload=None, retry=True):
        '''
        Execute HTTP POST
        '''
        headers = self._gen_headers(self.access_token, url)
        attempts = 1
        while attempts <= HTTP_ATTEMPTS_MAX:
            try:
                res = requests.post(url, headers=headers, data=payload,
                                    timeout=15, verify=self.certs)
                res.raise_for_status()
                if res.headers['Content-Length'] == '0':
                    return None
                else:
                    return res.json()
            except requests.exceptions.RequestException as e:
                attempts += 1
                if res.status_code in [400, 429]:
                    if res.json()['challenge']: 

                        ''' HANDLE CHALLENGE 2FA '''
                        url = 'https://api.robinhood.com/challenge/{}/respond/'.format(res.json()['challenge']['id'])
                        
                        validated, trys = False, 0
                        while validated == False:
                            trys += 1; print('Trys: {}.'.format(trys))
                            time.sleep(5) # wait until the email has been sent
                            challenge_res = requests.post(url, headers = headers, 
                                                          data = {'response' : self.fetch_mfa_code()}, timeout = 15, verify = self.certs)
                            try:
                                headers['X-ROBINHOOD-CHALLENGE-RESPONSE-ID'] = challenge_res.json()['id']
                                validated = True
                            except KeyError:
                                print(json.dumps(challenge_res.json(), indent = 4))
                                validated = False

                        ''' TRY TO FETCH REFRESH/ACCESS TOKENS '''
                        url = "https://api.robinhood.com/oauth2/token/"
                        challenge_res = requests.post(url, headers = headers,
                                                      data = payload, timeout = 15, verify = self.certs)
                        #print('Response from submitting 2nd challenge code: {}'.format(json.dumps(challenge_res.json(), indent = 4)))
                        
                        assert challenge_res is not None, print('Multi-factor challenge failed.')
                        return challenge_res.json()

                    else:    
                        raise e
                elif retry and res.status_code in [403]:
                    self.relogin_oauth2()


    def _gen_headers(self, bearer, url):
        '''
        Generate headders, adding in Oauth2 bearer token if present
        '''
        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en;q=1, fr;q=0.9, de;q=0.8, ja;q=0.7, nl;q=0.6, it;q=0.5",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",

        }
        if bearer:
            headers["Authorization"] = "Bearer {0}".format(bearer)
        if url == "https://api.robinhood.com/options/orders/":
            headers["Content-Type"] = "application/json; charset=utf-8"
        return headers


    def GenerateDeviceToken():
        rands = []
        for i in range(0,16):
            r = random.random()
            rand = 4294967296.0 * r
            rands.append((int(rand) >> ((3 & i) << 3)) & 255)

        hexa = []
        for i in range(0,256):
            hexa.append(str(hex(i+256)).lstrip("0x").rstrip("L")[1:])

        id = ""
        for i in range(0,16):
            id += hexa[rands[i]]

            if (i == 3) or (i == 5) or (i == 7) or (i == 9):
                id += "-"

        return id


    def fetch_mfa_code(self):
        username, password = user, pass

        obj = imaplib.IMAP4_SSL('imap.gmail.com')
        obj.login(username, password)
        obj.select()

        cutoff = (datetime.today() - timedelta(minutes = 2)).strftime('%d-%b-%Y')
        typ, data = obj.search(None, 
                    '(SINCE %s) (FROM "notifications@robinhood.com")' % (cutoff,))
        email_ids = data[0].decode().split(' ')
        email = obj.fetch(email_ids[-1], '(UID BODY[TEXT])')

        parsed = email[1][0][1].decode().split('r')[9]
        mfa_code = [int(s) for s in re.findall(pattern = r'\d+', string = parsed)]
        
        #assert len(str(mfa_code[0])) == 6
        if len(str(mfa_code[0])) != 6: mfa_code = '0' + str(mfa_code) # HACK: fix

        return mfa_code[0]


    def login_oauth2(self, username, password, mfa_code=None, id=None):
        '''
        Login using username and password
        '''
        self.username = username
        self.password = password

        if self.device_token == None: 
            self.device_token = self.GenerateDeviceToken()

        data = {
            "grant_type": "password",
            "scope": "internal",
            "client_id": CLIENT_ID,
            "expires_in": 86400,
            "password": password,
            "username": username,
            "device_token": self.device_token
        }

        url = "https://api.robinhood.com/oauth2/token/"
        res = self.post(url, payload = data, retry = False)

        if res is None:
            if mfa_code is None:
                msg = "Client.login_oauth2(). Could not authenticate. Check username and password."
                raise AuthenticationError(msg)
            else:
                msg = "Client.login_oauth2(). Could not authenticate. Check username and password, and enter a valid MFA code."
                raise AuthenticationError(msg)
        elif res.get('mfa_required') is True:
            msg = "Client.login_oauth2(). Could not authenticate. MFA is required."
            raise AuthenticationError(msg)

        self.access_token   = res["access_token"]
        self.refresh_token  = res["refresh_token"]
        self.mfa_code       = res["mfa_code"]
        self.scope          = res["scope"]
        self.__set_account_info()
        return self.authenticated


    def __set_account_info(self):
        account_urls = Account.all_urls(self)
        if len(account_urls) > 1:
            msg = "fast_arrow 'currently' does not handle multiple account authentication."
            raise NotImplementedError(msg)
        elif len(account_urls) == 0:
            msg = "fast_arrow expected at least 1 account."
            raise AuthenticationError(msg)
        else:
            self.account_url = account_urls[0]
            self.account_id = get_last_path(self.account_url)
            self.authenticated = True


    def relogin_oauth2(self):
        '''
        (Re)login using the Oauth2 refresh token
        '''
        url = "https://api.robinhood.com/oauth2/token/"
        data = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
            "scope": "internal",
            "client_id": CLIENT_ID,
            "expires_in": 86400,
        }
        res = self.post(url, payload=data, retry=False)
        self.access_token   = res["access_token"]
        self.refresh_token  = res["refresh_token"]
        self.mfa_code       = res["mfa_code"]
        self.scope          = res["scope"]


    def logout_oauth2(self):
        '''
        Logout for given Oauth2 bearer token
        '''
        url = "https://api.robinhood.com/oauth2/revoke_token/"
        data = {
            "client_id": CLIENT_ID,
            "token": self.refresh_token,
        }
        res = self.post(url, payload=data)
        if res == None:
            self.account_id     = None
            self.account_url    = None
            self.access_token   = None
            self.refresh_token  = None
            self.mfa_code       = None
            self.scope          = None
            self.authenticated  = False
            return True
        else:
            raise AuthenticationError("fast_arrow could not log out.")