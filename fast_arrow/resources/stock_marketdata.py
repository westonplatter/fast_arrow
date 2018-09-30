from fast_arrow.util import chunked_list


class StockMarketdata(object):

    @classmethod
    def quote_by_symbol(cls, symbol):
        """
        fetch and return results
        """
        return []

    @classmethod
    def quote_by_symbols(cls, symbols):
        """
        fetch and return results
        """
        return []
    # @classmethod
    # def quote_by_symbol(cls, client=None, symbol):
    #     '''
    #     fetch and return results
    #     '''
    #     return cls.quote_by_symbols(client, [symbol])[0]
    #
    #
    # @classmethod
    # def quote_by_symbols(cls, client=None, symbols):
    #     '''
    #     fetch and return results
    #     '''
    #     url = "https://api.robinhood.com/quotes/"
    #     params = {"symbols": ",".join(symbols)}
    #     return client.get(url, params=params)


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
