from fast_arrow.util import chunked_list


class OptionMarketdata(object):

    @classmethod
    def quote_by_instrument_id(cls, client, _id):
        return cls.quotes_by_instrument_ids(client, [_id])[0]


    @classmethod
    def quote_by_instrument_url(cls, client, url):
        return cls.quotes_by_instrument_urls(client, [url])[0]


    @classmethod
    def quotes_by_instrument_ids(cls, client, ids):
        """
        create instrument urls, fetch, return results
        """
        base_url = "https://api.robinhood.com/options/instruments/"
        id_urls = ["{}{}/".format(base_url, _id) for _id in ids]
        return cls.quotes_by_instrument_urls(client, id_urls)


    @classmethod
    def quotes_by_instrument_urls(cls, client, urls):
        """
        fetch and return results
        note - data requests are batched to limit urls to 50 per http request
        """
        results = []

        for _urls in chunked_list(urls, 50):
            url = "https://api.robinhood.com/marketdata/options/"
            params = {"instruments": ",".join(_urls)}
            data = client.get(url, params=params)

            partial_results = data["results"]

            while ("next" in data and data["next"]):
                data = get(data["next"], bearer=bearer)
                partial_results.extend(data["results"])

            results.extend(partial_results)

        return results
