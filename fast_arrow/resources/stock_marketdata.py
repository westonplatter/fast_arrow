from fast_arrow.util import chunked_list


class StockMarketdata(object):

    @classmethod
    def quote_by_symbol(cls, client, symbol):
        '''
        fetch and return results
        '''
        return cls.quote_by_symbols(client, [symbol])['results'][0]


    @classmethod
    def quote_by_symbols(cls, client, symbols):
        '''
        fetch and return results
        '''
        url = "https://api.robinhood.com/quotes/"
        params = {"symbols": ",".join(symbols)}
        return client.get(url, params=params)


    @classmethod
    def quotes_by_instrument_ids(cls, client, ids):
        """
        create instrument urls, fetch, return results
        """
        base_url = "https://api.robinhood.com/instruments/"
        id_urls = ["{}{}/".format(base_url, _id) for _id in ids]
        return cls.quotes_by_instrument_urls(client, id_urls)


    @classmethod
    def quotes_by_instrument_urls(cls, client, urls):
        """
        fetch and return results
        """
        instruments = ",".join(urls)
        params = {"instruments": instruments}
        url = "https://api.robinhood.com/marketdata/quotes/"
        data = client.get(url, params=params)
        results = data["results"]
        while "next" in data and data["next"]:
            data = client.get(data["next"], bearer=bearer)
            results.extend(data["results"])
        return results

    @classmethod
    def historical(cls, client, symbol, span="year", bounds="regular"):
        possible_intervals = {
            "day": "5minute",
            "week": "10minute",
            "year": "day",
            "5year": "week" }
        assert span in possible_intervals.keys()
        interval = possible_intervals[span]
        assert bounds in ["regular", "trading"]

        request_url = "https://api.robinhood.com/marketdata/historicals/{}/".format(symbol)
        params = {
            "span":     span,
            "interval": interval,
            "bounds":   bounds,
            "symbol":   symbol
        }
        data = client.get(request_url, params=params)
        return data
