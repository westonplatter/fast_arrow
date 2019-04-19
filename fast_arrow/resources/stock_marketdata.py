from fast_arrow.util import chunked_list
import deprecation
from fast_arrow.version import VERSION


class StockMarketdata(object):

    @classmethod
    def quote_by_instrument(cls, client, _id):
        return cls.quote_by_instruments(client, [_id])[0]

    @classmethod
    def quote_by_instruments(cls, client, ids):
        """
        create instrument urls, fetch, return results
        """
        base_url = "https://api.robinhood.com/instruments"
        id_urls = ["{}/{}/".format(base_url, _id) for _id in ids]
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
            data = client.get(data["next"])
            results.extend(data["results"])
        return results

    @classmethod
    @deprecation.deprecated(
        deprecated_in="0.3.1", removed_in="0.4", current_version=VERSION,
        details="Use 'historical_quote_by_symbol' instead")
    def historical(cls, client, symbol, span="year", bounds="regular"):
        return cls.historical_quote_by_symbol(client, symbol, span, bounds)

    @classmethod
    def historical_quote_by_symbol(cls, client, symbol, span="year",
                                   bounds="regular"):
        datas = cls.historical_quote_by_symbols(client, [symbol], span, bounds)
        return datas[0]

    @classmethod
    def historical_quote_by_symbols(cls, client, symbols, span="year",
                                    bounds="regular"):
        possible_intervals = {
            "day": "5minute",
            "week": "10minute",
            "year": "day",
            "5year": "week"}
        assert span in possible_intervals.keys()
        interval = possible_intervals[span]
        assert bounds in ["regular"]

        request_url = "https://api.robinhood.com/marketdata/historicals/"

        results = []
        for _symbols in chunked_list(symbols, 25):
            params = {"span": span, "interval": interval, "bounds": bounds,
                      "symbols": ",".join(_symbols)}
            data = client.get(request_url, params=params)
            if data and data["results"]:
                results.extend(data["results"])
        return results
