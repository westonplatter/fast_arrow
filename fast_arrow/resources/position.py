from fast_arrow.api_requestor import get


class Position(object):

    @classmethod
    def all(cls, token):
        """
        fetch all positions
        """
        url = 'https://api.robinhood.com/positions/'
        positions = []

        data = get(url, token)
        positions.extend(data["results"])
        while data["next"]:
            data = get(data["next"], token)
            positions.extend(data["results"])
        return positions
