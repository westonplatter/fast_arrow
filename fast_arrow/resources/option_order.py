from fast_arrow.api_requestor import get
from fast_arrow import util
from fast_arrow.resources.option import Option


class OptionOrder(object):

    @classmethod
    def all(cls, token):
        """
        fetch all option positions
        """
        url = 'https://api.robinhood.com/options/orders/'
        data = get(url, token=token)
        results = data["results"]
        while data["next"]:
            data = get(data["next"], token)
            results.extend(data["results"])
        return results
