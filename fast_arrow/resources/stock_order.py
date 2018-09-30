
class StockOrder(object):

    @classmethod
    def all(cls, client):
        """"
        fetch data for multiple stocks
        """
        url = "https://api.robinhood.com/orders/"
        data = client.get(url)
        results = data["results"]
        while data["next"]:
            data = client.get(data["next"])
            results.extend(data["results"])
        return results
