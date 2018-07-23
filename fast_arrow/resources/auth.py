import fast_arrow
from fast_arrow.api_requestor import post


class Auth(object):
    @classmethod
    def login(cls, username, password, mfa_code=None):
        url = 'https://api.robinhood.com/api-token-auth/'

        payload = {
            'username': username,
            'password': password
        }
        if mfa_code:
            payload['mfa_code'] = mfa_code

        resj = post(url, None, payload)

        if 'token' in resj.keys():
            return resj['token']


    @classmethod
    def logout(cls):
        url = 'https://api.robinhood.com/api-token-logout/'
        resj = post(login_url(), timeout=15)
        return resj
