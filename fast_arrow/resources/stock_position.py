
class StockPosition(object):

    @classmethod
    def all(cls, client):
        url = "https://api.robinhood.com/positions/"
        data = client.get(url)
        results = data["results"]
        while data["next"]:
            data = get(data["next"], token=token)
            results.extend(data["results"])
        return results
