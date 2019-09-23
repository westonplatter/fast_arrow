from fast_arrow.version import VERSION
from fast_arrow.exceptions import ApiDoesNotSupportError
from fast_arrow.resources.stock_marketdata import StockMarketdata

import deprecation


class Stock(object):

    @classmethod
    @deprecation.deprecated(
        deprecated_in="1.0.0",
        removed_in="1.1",
        current_version=VERSION,
        details="Use 'StockMarketdata.quote_by_symbol'")
    def fetch(cls, client, symbol):
        message = '''
            Robinhood API seems to not support this endpoint.
            Use fast_arrow.StockMarketdata.quote_by_symbol
        '''
        raise ApiDoesNotSupportError(message)

    @classmethod
    @deprecation.deprecated(
        deprecated_in="1.0.0",
        removed_in="1.1",
        current_version=VERSION,
        details="Use 'StockMarketdata.quote_by_symbols'")
    def all(cls, client, symbols):
        message = '''
            Robinhood API seems to not support this endpoint.
            Use fast_arrow.StockMarketdata.quote_by_symbols
        '''
        raise ApiDoesNotSupportError(message)

    @classmethod
    def mergein_marketdata_list(cls, client, stocks):
        ids = [x["id"] for x in stocks]
        mds = StockMarketdata.quote_by_instruments(client, ids)
        mds = [x for x in mds if x]

        results = []
        for s in stocks:
            # @TODO optimize this so it's better than O(n^2)
            md = [md for md in mds if md['instrument'] == s['url']]
            if len(md) > 0:
                md = md[0]
                md_kv = {
                    "ask_price": md["ask_price"],
                    "bid_price": md["bid_price"],
                }
                merged_dict = dict(list(s.items()) + list(md_kv.items()))
            else:
                merged_dict = dict(list(s.items()))
            results.append(merged_dict)
        return results

    @classmethod
    def popularity(cls, client, instrument_ids):
        url = "https://api.robinhood.com/instruments/popularity/"
        params = {"ids": ",".join(instrument_ids)}
        data = client.get(url, params)
        results = data["results"]
        while data["next"]:
            data = client.get(data["next"])
            results.extend(data["results"])
        return results
