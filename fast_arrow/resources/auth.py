import fast_arrow
from fast_arrow.api_requestor import post


class Auth(object):
    @classmethod
    def login(cls, username, password, mfa_code=None):
        """
        Login with username, password, and optionally MFA
        """
        url = 'https://api.robinhood.com/api-token-auth/'

        payload = {
            'username': username,
            'password': password
        }
        if mfa_code:
            payload['mfa_code'] = mfa_code

        resj = post(url, payload=payload)

        if 'token' in resj.keys():
            return resj['token']


    @classmethod
    def get_oauth_token(cls, token):
        """
        get OAuth2 Bearer token from token
        """
        url = "https://api.robinhood.com/oauth2/migrate_token/"
        res = post(url, token=token)
        oauth_token = res["access_token"]
        return oauth_token


    @classmethod
    def logout(cls, token):
        """
        Logout for given token
        """
        url = 'https://api.robinhood.com/api-token-logout/'
        data = post(url, token=token, timeout=15)
        return data
