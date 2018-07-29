from fast_arrow.api_requestor import get


class OptionChain(object):

    @classmethod
    def fetch(cls, bearer, id):
        """
        fetch option chain for instrument
        """
        url = "https://api.robinhood.com/options/chains/"
        params = {
            "equity_instrument_ids": [id],
            "state": "active",
            "tradability": "tradable"
        }
        data = get(url, bearer=bearer, params=params)
        return data['results'][0]
