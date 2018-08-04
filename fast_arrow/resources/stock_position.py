from fast_arrow.api_requestor import get


class StockPosition(object):

    @classmethod
    def all(cls, token):
        url = "https://api.robinhood.com/positions/"
        data = get(url, token=token)
        results = data["results"]
        while data["next"]:
            data = get(data["next"], token=token)
            results.extend(data["results"])
        return results
