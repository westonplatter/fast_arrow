from fast_arrow.api_requestor import get


class OptionEvent(object):

    @classmethod
    def all(cls, bearer):
        """
        fetch all option positions
        """
        url = 'https://api.robinhood.com/options/events/'
        params = { }
        data = get(url, bearer=bearer, params=params)
        results = data["results"]
        while data["next"]:
            data = get(data["next"], token)
            results.extend(data["results"])
        return results
