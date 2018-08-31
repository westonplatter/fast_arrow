from fast_arrow.util import chunked_list
from fast_arrow.resources.option_marketdata import OptionMarketdata
from fast_arrow.exceptions import NotImplementedError


class Option(object):

    @classmethod
    def fetch_by_url(cls, client, url):
        return cls.instrument_by_urls(client, [url])


    @classmethod
    def fetch_by_urls(cls, client, urls):
        raise NotImplementedError("Option.instrument_by_url")


    @classmethod
    def fetch_by_ids(cls, client, ids):
        results = []
        params = {"ids": ",".join(ids)}
        request_url = "https://api.robinhood.com/options/instruments/"
        data = client.get(request_url, params=params)
        results = data["results"]
        while data["next"]:
            data = client.get(data["next"])
            results.extend(data["results"])
        return results

    @classmethod
    def fetch_by_id(cls, bearer, _id):
        return cls.fetch_by_ids(bearer, [_id])

    # deprecate me
    @classmethod
    def fetch(cls, client, _id):
        """
        fetch by instrument id
        """
        return cls.fetch_list(client, [_id])[0]

    #
    # @TODO depricate me
    #
    @classmethod
    def fetch_list(cls, client, ids):
        """
        fetch instruments by ids
        """
        results = []
        request_url = "https://api.robinhood.com/options/instruments/"

        for _ids in chunked_list(ids, 50):

            params = {"ids": ",".join(_ids)}
            data = client.get(request_url, params=params)
            partial_results = data["results"]

            while data["next"]:
                data = client.get(data["next"])
                partial_results.extend(data["results"])
            results.extend(partial_results)

        return results


    @classmethod
    def in_chain(cls, client, chain_id, expiration_dates=[]):
        """
        fetch all option instruments in an options chain
        - expiration_dates = optionally scope
        """

        request_url = "https://api.robinhood.com/options/instruments/"
        params = {
            "chain_id": chain_id,
            "expiration_dates": ",".join(expiration_dates)
        }

        data = client.get(request_url, params=params)
        results = data['results']

        while data['next']:
            data = client.get(data['next'])
            results.extend(data['results'])
        return results


    @classmethod
    def mergein_marketdata_list(cls, client, options):
        ids = [x["id"] for x in options]
        mds = OptionMarketdata.quotes_by_instrument_ids(client, ids)
        mds = [x for x in mds if x]

        results = []
        for o in options:
            # @TODO optimize this so it's better than O(n^2)
            md = [md for md in mds if md['instrument'] == o['url']]
            if len(md)>0:
                md = md[0]
                # there is no overlap in keys, so it's fine to do a merge
                merged_dict = dict( list(o.items()) + list(md.items()) )
            else:
                merged_dict = dict( list(o.items()) )
            results.append(merged_dict)

        return results
