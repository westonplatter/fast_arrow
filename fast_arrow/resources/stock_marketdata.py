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
        """
        instruments = ",".join(urls)
        params = {"instruments": instruments}
        data = client.get(url, bearer=bearer)
        results = data["results"]
        while data["next"]:
            data = get(data["next"], bearer=bearer)
            results.extend(data["results"])
        return results
