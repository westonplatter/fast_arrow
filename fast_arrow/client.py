import requests
from fast_arrow.resources.user import User
from fast_arrow.exceptions import AuthenticationError
from fast_arrow.exceptions import NotImplementedError


CLIENT_ID = "c82SH0WZOsabOXGP2sxqcj34FxkvfnWRZBKlBjFS"


class Client(object):

    def __init__(self, **kwargs):
        self.options = kwargs
        self.access_token   = None
        self.refresh_token  = None
        self.mfa_code       = None
        self.scope          = None
        self.authenticated  = False

    def authenticate(self):
        """
        Authenticate using data in `options`
        """
        if "username" in self.options and "password" in self.options:
            return self.login_oauth2(self.options["username"], self.options["password"])

        elif "access_token" in self.options and "refresh_token" in self.options:
            self.access_token = self.options["access_token"]
            self.refresh_token = self.options["refresh_token"]
            # if we get HTTP 403, catch and raise error
            user = User.fetch(self)
            return True

        else:
            self.authenticated = False


    def get(self, url=None, params=None):
        """
        Execute HTTP GET
        """
        headers = self._gen_headers(self.access_token)

        attempts = 1
        while attempts:
            try:
                res = requests.get(url, headers=headers, params=params, timeout=15)
                return res.json()
            except:
                self.relogin_oauth2()
                attempts -= 1
            else:
                attempts = False


    def post(self, url=None, payload=None):
        """
        Execute HTTP POST
        """
        headers = self._gen_headers(self.access_token)
        attempts = 1
        while attempts:
            try:
                res = requests.post(url, headers=headers, data=payload, timeout=15)
                if res.headers['Content-Length'] == '0':
                    return None
                else:
                    return res.json()
            except:
                self.relogin_oauth2()
                attempts -= 1
            else:
                attempts = False


    def _gen_headers(self, bearer):
        """
        Generate headders, adding in Oauth2 bearer token if present
        """
        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en;q=1, fr;q=0.9, de;q=0.8, ja;q=0.7, nl;q=0.6, it;q=0.5",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
        }
        if bearer:
            headers["Authorization"] = "Bearer {0}".format(bearer)
        return headers


    def login_oauth2(self, username, password):
        """
        Login using username and password
        """
        data = {
            "grant_type": "password",
            "scope": "internal",
            "client_id": CLIENT_ID,
            "expires_in": 86400,
            "password": password,
            "username": username
        }
        url = "https://api.robinhood.com/oauth2/token/"
        res = self.post(url, payload=data)
        self.access_token   = res["access_token"]
        self.refresh_token  = res["refresh_token"]
        self.mfa_code       = res["mfa_code"]
        self.scope          = res["scope"]
        self.authenticated  = True
        return True


    def relogin_oauth2(self):
        """
        (Re)login using the Oauth2 refresh token
        """
        url = "https://api.robinhood.com/oauth2/token/"
        data = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
            "scope": "internal",
            "client_id": CLIENT_ID,
            "expires_in": 86400,
        }
        res = self.post(url, payload=data)
        self.access_token   = res["access_token"]
        self.refresh_token  = res["refresh_token"]
        self.mfa_code       = res["mfa_code"]
        self.scope          = res["scope"]
        self.authenticated  = True
        return True


    def logout_oauth2(self):
        """
        Logout for given Oauth2 bearer token
        """
        url = "https://api.robinhood.com/oauth2/revoke_token/"
        data = {
            "client_id": CLIENT_ID,
            "token": self.refresh_token,
        }
        res = self.post(url, payload=data)
        result = (True if res == None else False)
        self.authenticated = False
        return result
