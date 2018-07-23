from fast_arrow.api_requestor import get


class User(object):

    @classmethod
    def fetch(cls, token):
        url = 'https://api.robinhood.com/user/'
        resj = get(url, token=token)
        return resj
