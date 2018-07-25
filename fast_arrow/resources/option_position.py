from fast_arrow.api_requestor import get


class OptionPosition(object):

    @classmethod
    def all(cls, token):
        """
        fetch all option positions
        NOTE: http response body is a list, not a dictionary like "positions"
        """
        url = 'https://api.robinhood.com/options/positions/'
        option_positions = get(url, token)
        return option_positions
