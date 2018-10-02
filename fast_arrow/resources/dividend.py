
class Dividend(object):

    @classmethod
    def all(cls, client):
        """"
        fetch data for dividends
        """
        url = "https://api.robinhood.com/dividends/"
        data = client.get(url)
        results = data["results"]
        while data["next"]:
            data = client.get(data["next"])
            results.extend(data["results"])
        return results
