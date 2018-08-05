from fast_arrow.api_requestor import get


class Option(object):

    @classmethod
    def fetch(cls, bearer, _id):
        """
        fetch instrument
        """
        return cls.fetch_list(bearer, [_id])[0]


    @classmethod
    def fetch_list(cls, bearer, ids):
        """
        fetch instruments
        """
        param_ids = ",".join(ids)
        params = {"ids": param_ids}

        url = "https://api.robinhood.com/options/instruments/"
        data = get(url, bearer=bearer, params=params)
        results = data["results"]

        while data["next"]:
            data = get(data["next"], bearer=bearer)
            results.extend(data["results"])
        return results


    @classmethod
    def marketdata(cls, bearer, _id):
        """
        fetch option market data (like Delta, Theta, Rho, Vega, Open Interest)
        """
        return cls.marketdata_list(bearer, [_id])[0]


    @classmethod
    def marketdata_list(cls, bearer, ids):
        """
        fetch option market data (like Delta, Theta, Rho, Vega, Open Interest)
        """
        # build params
        base_marketdata_url = "https://api.robinhood.com/options/instruments/"
        id_urls = []
        for _id in ids:
            id_url = "{}{}/".format(base_marketdata_url, _id)
            id_urls.append(id_url)

        instruments = ",".join(id_urls)
        params = {"instruments": instruments}

        # fetch
        url = "https://api.robinhood.com/marketdata/options/"
        data = get(url, bearer=bearer, params=params)
        results = data["results"]

        if "next" in data:
            while(data["next"]):
                data = get(data["next"], bearer=bearer)
                results.extend(data["results"])
        return results


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
