from fast_arrow.resources.stock_marketdata import StockMarketdata

class Stock(object):

    @classmethod
    def fetch(cls, client, symbol):
        """
        fetch data for stock
        """
        assert(type(symbol) is str)

        url = "https://api.robinhood.com/instruments/?symbol={0}".format(symbol)
        data = client.get(url)
        return data["results"][0]

    @classmethod
    def mergein_marketdata_list(cls, client, stocks):
        ids = [x["id"] for x in stocks]
        mds = StockMarketdata.quotes_by_instrument_ids(client, ids)
        mds = [x for x in mds if x]

        results = []
        for s in stocks:
            # @TODO optimize this so it's better than O(n^2)
            md = [md for md in mds if md['instrument'] == s['url']]
            if len(md)>0:
                md = md[0]
                md_kv = {
                    "ask_price": md["ask_price"],
                    "bid_price": md["bid_price"],
                }
                merged_dict = dict( list(s.items()) + list(md_kv.items()) )
            else:
                merged_dict = dict( list(s.items()) )
            results.append(merged_dict)
        return results


    @classmethod
    def all(cls, client, symbols):
        """"
        fetch data for multiple stocks
        """
        params = {"symbol": ",".join(symbols)}
        request_url = "https://api.robinhood.com/instruments/"

        data = client.get(request_url, params=params)
        results = data["results"]

        while data["next"]:
            data = client.get(data["next"], bearer=bearer)
            results.extend(data["results"])
        return results
