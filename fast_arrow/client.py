import os
import requests
from fast_arrow.util import get_last_path
from fast_arrow.resources.user import User
from fast_arrow.resources.account import Account
from fast_arrow.exceptions import AuthenticationError
from fast_arrow.exceptions import NotImplementedError


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
                if retry and res.status_code in [403]:
                    self.relogin_oauth2()


    def post(self, url=None, payload=None, retry=True):
        '''
        Execute HTTP POST
        '''
        headers = self._gen_headers(self.access_token, url)
        attempts = 1
        while attempts <= HTTP_ATTEMPTS_MAX:
            try:
                res = requests.post(url, headers=headers, data=payload, timeout=15, verify=self.certs)
                res.raise_for_status()
                if res.headers['Content-Length'] == '0':
                    return None
                else:
                    return res.json()
            except requests.exceptions.RequestException as e:
                attempts += 1
                if retry and res.status_code in [403]:
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


    def login_oauth2(self, username, password, mfa_code=None):
        '''
        Login using username and password
        '''
        data = {
            "grant_type": "password",
            "scope": "internal",
            "client_id": CLIENT_ID,
            "expires_in": 86400,
            "password": password,
            "username": username
        }
        if mfa_code is not None:
            data['mfa_code'] = mfa_code
        url = "https://api.robinhood.com/oauth2/token/"
        res = self.post(url, payload=data, retry=False)

        if res is None:
            if mfa_code is None:
                raise AuthenticationError("Client.login_oauth2(). Could not authenticate. Check username and password.")
            else:
                raise AuthenticationError("Client.login_oauth2(). Could not authenticate. Check username and password, and enter a valid MFA code.")
        elif res.get('mfa_required') is True:
            raise AuthenticationError("Client.login_oauth2(). Could not authenticate. MFA is required.")

        self.access_token   = res["access_token"]
        self.refresh_token  = res["refresh_token"]
        self.mfa_code       = res["mfa_code"]
        self.scope          = res["scope"]
        self.__set_account_info()
        return self.authenticated


    def __set_account_info(self):
        account_urls = Account.all_urls(self)
        if len(account_urls) > 1:
            raise NotImplementedError("fast_arrow 'currently' does not handle multiple account authentication.")
        elif len(account_urls) == 0:
            raise AuthenticationError("fast_arrow expected at least 1 account.")
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
