from fast_arrow.api_requestor import get


class Stock(object):

    @classmethod
    def fetch(cls, bearer, symbol):
        """
        fetch data for stock
        """
        assert(type(symbol) is str)

        url = "https://api.robinhood.com/instruments/?symbol={0}".format(symbol)
        data = get(url, bearer=bearer)
        return data["results"][0]

    @classmethod
    def quote_by_instrument_id(cls, _id):
        return []

    @classmethod
    def all(cls, bearer, symbols):
        """"
        fetch data for multiple stocks
        """
        params = {"symbol": ",".join(symbols)}
        request_url = "https://api.robinhood.com/instruments/"

        data = get(request_url, bearer=bearer, params=params)
        results = data["results"]

        while data["next"]:
            data = get(data["next"], bearer=bearer)
            results.extend(data["results"])
        return results
