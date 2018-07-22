import fast_arrow

from fast_arrow.api_requestor import gen_url, http_get, http_post

class Session(object):

    @classmethod
    def login(cls, username, password, mfa_code=None):
        payload = {
            'username': username,
            'password': password
        }

        if mfa_code:
            payload['mfa_code'] = mfa_code

        resj = http_post(gen_url('login'), None, payload)

        if 'token' in resj.keys():
            return resj['token']

    @classmethod
    def logout(cls):
         resj = http_post(gen_url('logout'), timeout=15)
         return resj
