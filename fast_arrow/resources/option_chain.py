class OptionChain(object):

    @classmethod
    def fetch(cls, client, _id, symbol):
        """
        fetch option chain for instrument
        """
        url = "https://api.robinhood.com/options/chains/"
        params = {
            "equity_instrument_ids": _id,
            "state": "active",
            "tradability": "tradable"
        }
        data = client.get(url, params=params)
        def filter_func(x):
            return x["symbol"] == symbol
        results = list(filter(filter_func, data["results"]))
        return results[0]
