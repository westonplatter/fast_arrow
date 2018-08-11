from fast_arrow.api_requestor import get
from fast_arrow.util import chunked_list


class OptionMarketdata(object):

    @classmethod
    def quote_by_instrument_id(cls, bearer, _id):
        return cls.quotes_by_instrument_ids(bearer, [_id])[0]


    @classmethod
    def quote_by_instrument_url(cls, bearer, url):
        return cls.quotes_by_instrument_urls(bearer, [url])[0]


    @classmethod
    def quotes_by_instrument_ids(cls, bearer, ids):
        """
        create instrument urls, fetch, return results
        """
        base_url = "https://api.robinhood.com/options/instruments/"
        id_urls = ["{}{}/".format(base_url, _id) for _id in ids]
        return cls.quotes_by_instrument_urls(bearer, id_urls)


    @classmethod
    def quotes_by_instrument_urls(cls, bearer, urls):
        """
        fetch and return results
        note - data requests are batched to limit urls to 50 per http request
        """
        results = []

        for _urls in chunked_list(urls, 50):
            url = "https://api.robinhood.com/marketdata/options/"
            params = {"instruments": ",".join(_urls)}
            data = get(url, bearer=bearer, params=params)

            partial_results = data["results"]

            while ("next" in data and data["next"]):
                data = get(data["next"], bearer=bearer)
                partial_results.extend(data["results"])

            results.extend(partial_results)

        return results
