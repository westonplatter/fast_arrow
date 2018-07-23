from fast_arrow.api_requestor import get


class Position(object):

    @classmethod
    def all(cls, token):
        url = 'https://api.robinhood.com/positions/'
        resj = get(url, token)
        return resj
