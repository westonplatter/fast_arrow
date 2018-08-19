from fast_arrow.api_requestor import get


class User(object):

    @classmethod
    def fetch(cls, client):
        url = 'https://api.robinhood.com/user/'
        res = get(url, client)
        return res
