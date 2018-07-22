from fast_arrow.api_requestor import http_get, gen_url

class User(object):

    @classmethod
    def fetch(cls, token):
        data = http_get(gen_url('user'), token=token)
        return data
