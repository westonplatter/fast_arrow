import os
import requests
from fast_arrow.util import get_last_path
from fast_arrow.resources.account import Account
from fast_arrow.exceptions import AuthenticationError
from fast_arrow.exceptions import NotImplementedError
from fast_arrow.exceptions import AuthDataError

HTTP_ATTEMPTS_MAX = 2

CLIENT_ID = "c82SH0WZOsabOXGP2sxqcj34FxkvfnWRZBKlBjFS"

class Client(object):

    def __init__(self, auth_data):
        required_keys = [
            "account_id",
            "access_token",
            "refresh_token",
            "device_token"
        ]

        for k in required_keys:
            if k not in auth_data:
                msg = "Expected key={} not in auth_data".format(k)
                raise AuthDataError(msg)

        self.auth_data = auth_data
        self.account_id = auth_data["account_id"]
        self.access_token = auth_data["access_token"]
        self.refresh_token = auth_data["refresh_token"]
        self.device_token = auth_data["device_token"]
        certs_path = 'ssl_certs/certs.pem'
        self.certs = os.path.join(os.path.dirname(__file__), certs_path)


    def get(self, url=None, params=None, retry=True):
        '''
        Execute HTTP GET
        '''
        headers = self._gen_headers(self.access_token, url)
        attempts = 1
        while attempts <= HTTP_ATTEMPTS_MAX:
            try:
                res = requests.get(url,
                                   headers=headers,
                                   params=params,
                                   timeout=15,
                                   verify=self.certs)
                res.raise_for_status()
                return res.json()
            except requests.exceptions.RequestException as e:
                attempts += 1
                if res.status_code in [400, 401]:
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
                res = requests.post(url,
                                    headers=headers,
                                    data=payload,
                                    timeout=15,
                                    verify=self.certs)
                res.raise_for_status()
                if res.headers['Content-Length'] == '0':
                    return None
                else:
                    return res.json()
            except requests.exceptions.RequestException as e:
                attempts += 1
                if res.status_code in [400, 429]:
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
            "Accept-Language": ("en;q=1, fr;q=0.9, de;q=0.8, ja;q=0.7, " +
                                "nl;q=0.6, it;q=0.5"),
            "User-Agent": ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) " +
                           "AppleWebKit/537.36 (KHTML, like Gecko) " +
                           "Chrome/68.0.3440.106 Safari/537.36"),

        }
        if bearer:
            headers["Authorization"] = "Bearer {0}".format(bearer)
        if url == "https://api.robinhood.com/options/orders/":
            headers["Content-Type"] = "application/json; charset=utf-8"
        return headers

    def current_auth_data(self):
        auth_data = {
            "account_id": self.account_id,
            "access_token": self.access_token,
            "refresh_token": self.refresh_token,
            "device_token": self.device_token,
        }
        return auth_data

    def __set_account_info(self):
        account_urls = Account.all_urls(self)
        if len(account_urls) > 1:
            msg = ("fast_arrow 'currently' does not handle " +
                   "multiple account authentication.")
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
            "device_token": self.device_token,
            "refresh_token": self.refresh_token,
            "scope": "internal",
            "client_id": CLIENT_ID,
            "expires_in": 86400,
        }
        data = self.post(url, payload=data, retry=False)
        self.access_token = data["access_token"]
        self.refresh_token = data["refresh_token"]
        self.scope = data["scope"]
        return True

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
        if res is None or res == {}:
            self.account_id = None
            self.account_url = None
            self.access_token = None
            self.refresh_token = None
            self.mfa_code = None
            self.scope = None
            self.authenticated = False
            return True
        else:
            raise AuthenticationError("fast_arrow could not log out.")
