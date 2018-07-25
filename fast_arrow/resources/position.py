from fast_arrow.api_requestor import get


class Position(object):

    @classmethod
    def all(cls, token):
        """
        fetch all positions
        """
        url = 'https://api.robinhood.com/positions/'
        positions = []

        resj = get(url, token)
        positions.extend(resj["results"])
        while resj["next"]:
            resj = get(resj["next"], token)
            positions.extend(resj["results"])
        return positions
