from fast_arrow.api_requestor import get


class User(object):

    @classmethod
    def fetch(cls, client):
        url = 'https://api.robinhood.com/user/'
        res = client.get(url)
        return res
