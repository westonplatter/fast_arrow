class OptionChain(object):

    @classmethod
    def fetch(cls, client, id):
        """
        fetch option chain for instrument
        """
        url = "https://api.robinhood.com/options/chains/"
        params = {
            "equity_instrument_ids": [id],
            "state": "active",
            "tradability": "tradable"
        }
        data = client.get(url, params=params)
        return data['results'][0]
