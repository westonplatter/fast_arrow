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


    # @classmethod
    # def all_marketdata(cls, bearer, ids):
    #     """
    #     """
    #     url = "https://api.robinhood.com/marketdata/options/"
    #
    #     id_urls = []
    #     for id in ids:
    #         id_urls.append("https://api.robinhood.com/options/instruments/{0}/".format(id))
    #     params = {"instruments": ",".join(id_urls)}
    #     data = get(url, bearer=bearer, params=params)
    #     results = data["results"]
    #     while data["next"]:
    #         data = get(data["next"], bearer=bearer)
    #         results.extend(data["results"])


    @classmethod
    def all(cls, bearer, chain_id, expiration_dates):
        """
        fetch all options in a options chain for given expiration dates
        """
        assert(type(expiration_dates) is list)

        url = "https://api.robinhood.com/options/instruments/"
        params = {
            "chain_id": chain_id,
            "expiration_dates": ",".join(expiration_dates)
        }
        data = get(url, bearer=bearer, params=params)
        results = data['results']
        while data['next']:
            data = get(data['next'], bearer=bearer)
            results.extend(data['results'])
        return results
