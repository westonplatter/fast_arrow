from fast_arrow.api_requestor import get


class StockOrder(object):

    @classmethod
    def all(cls, token):
        """"
        fetch data for multiple stocks
        """
        url = "https://api.robinhood.com/orders/"
        data = get(url, token=token)
        results = data["results"]
        while data["next"]:
            data = get(data["next"], token=token)
            results.extend(data["results"])
        return results
