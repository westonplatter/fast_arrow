from fast_arrow.api_requestor import get


class Option(object):

    @classmethod
    def fetch(cls, bearer, id):
        """
        fetch instrument
        """
        url = "https://api.robinhood.com/options/instruments/{0}/".format(id)
        return get(url, bearer=bearer)


    @classmethod
    def marketdata(cls, bearer, id):
        """
        fetch option market data (like Strike Price, Delta, Theta, etc)
        """
        url = "https://api.robinhood.com/marketdata/options/"
        id_url = "https://api.robinhood.com/options/instruments/{0}/".format(id)
        params = {"instruments": id_url}
        data = get(url, bearer=bearer, params=params)
        return data["results"][0]
