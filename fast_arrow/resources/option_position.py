from fast_arrow.api_requestor import get


class OptionPosition(object):

    @classmethod
    def all(cls, token):
        url = 'https://api.robinhood.com/options/positions/'
        resj = get(url, token)
        return resj
