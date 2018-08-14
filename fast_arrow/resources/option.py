from fast_arrow.api_requestor import get
from fast_arrow.util import chunked_list
from fast_arrow.resources.option_marketdata import OptionMarketdata


class Option(object):

    @classmethod
    def fetch_by_ids(cls, bearer, ids):
        results = []
        params = {"ids": ",".join(ids)}
        request_url = "https://api.robinhood.com/options/instruments/"
        data = get(request_url, bearer=bearer, params=params)
        results = data["results"]
        while data["next"]:
            data = get(data["next"], bearer=bearer)
            results.extend(data["results"])
        return results


    # deprecate me
    @classmethod
    def fetch(cls, bearer, _id):
        """
        fetch by instrument id
        """
        return cls.fetch_list(bearer, [_id])[0]


    # deprecate me
    @classmethod
    def fetch_list(cls, bearer, ids):
        """
        fetch instruments by ids
        """
        results = []
        request_url = "https://api.robinhood.com/options/instruments/"

        for _ids in chunked_list(ids, 50):

            params = {"ids": ",".join(_ids)}
            data = get(request_url, bearer=bearer, params=params)
            partial_results = data["results"]

            while data["next"]:
                data = get(data["next"], bearer=bearer)
                partial_results.extend(data["results"])
            results.extend(partial_results)

        return results


    @classmethod
    def in_chain(cls, bearer, chain_id, expiration_dates=[]):
        """
        fetch all option instruments in an options chain
        - expiration_dates = optionally scope
        """

        request_url = "https://api.robinhood.com/options/instruments/"
        params = {
            "chain_id": chain_id,
            "expiration_dates": ",".join(expiration_dates)
        }

        data = get(request_url, bearer=bearer, params=params)
        results = data['results']

        while data['next']:
            data = get(data['next'], bearer=bearer)
            results.extend(data['results'])
        return results


    @classmethod
    def mergein_marketdata_list(cls, bearer, options):
        ids = [x["id"] for x in options]
        mds = OptionMarketdata.quotes_by_instrument_ids(bearer, ids)

        results = []
        for o in options:
            # @TODO optimize this so it's better than O(n^2)
            md = [md for md in mds if md['instrument'] == o['url']][0]
            # there is overlap in keys, so it's fine to do a merge
            merged_dict = dict( list(o.items()) + list(md.items()) )
            results.append(merged_dict)

        return results
