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
    def all(cls, bearer, symbols):
        """"
        fetch data for multiple stocks
        """
        assert(type(symbols) is list)

        symbole_str = ",".join(symbols)
        url = "https://api.robinhood.com/instruments/?symbol={0}".format(symbole_str)
        data = get(url, bearer=bearer)
        results = data["results"]
        while data["next"]:
            data = get(data["next"], bearer=bearer)
            results.extend(data["results"])
        return results
