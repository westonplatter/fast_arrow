from fast_arrow.util import chunked_list


class OptionMarketdata(object):

    @classmethod
    def quote_by_instrument_id(cls, client, _id):
        return cls.quotes_by_instrument_ids(client, [_id])[0]


    @classmethod
    def quotes_by_instrument_ids(cls, client, ids):
        base_url = "https://api.robinhood.com/options/instruments/"
        id_urls = ["{}{}/".format(base_url, _id) for _id in ids]
        return cls.quotes_by_instrument_urls(client, id_urls)


    @classmethod
    def quote_by_instrument_url(cls, client, url):
        return cls.quotes_by_instrument_urls(client, [url])[0]


    @classmethod
    def quotes_by_instrument_urls(cls, client, urls):
        results = []
        for _urls in chunked_list(urls, 50):
            url = "https://api.robinhood.com/marketdata/options/"
            params = {"instruments": ",".join(_urls)}
            data = client.get(url, params=params)
            if data and "results" in data:
                partial_results = data["results"]
                while ("next" in data and data["next"]):
                    data = get(data["next"], bearer=bearer)
                    partial_results.extend(data["results"])
                results.extend(partial_results)
        return results


    @classmethod
    def historical_quote_by_id(cls, client, _id, span="year"):
        return cls.historical_quotes_by_ids(client, [_id], span)[0]


    @classmethod
    def historical_quotes_by_ids(cls, client, ids, span="year"):
        base_url = "https://api.robinhood.com/options/instruments/"
        urls = ["{}{}/".format(base_url, _id) for _id in ids]
        return cls.historical_quotes_by_urls(client, urls)


    @classmethod
    def historical_quote_by_url(cls, client, url, span="year"):
        return cls.historical_quotes_by_urls(client, [url], span)[0]


    @classmethod
    def historical_quotes_by_urls(cls, client, urls, span="year"):
        possible_intervals = {
            "day": "5minute",
            "week": "10minute",
            "year": "day",
            "5year": "week" }
        assert span in possible_intervals.keys()
        interval = possible_intervals[span]
        results = []
        request_url = "https://api.robinhood.com/marketdata/options/historicals/"
        for _urls in chunked_list(urls, 5):
            params = { "span": span, "interval": interval, "instruments": ",".join(_urls) }
            data = client.get(request_url, params=params)
            if data and data["results"]:
                results.extend(data["results"])
        return results
