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

    @classmethod
    def humanize_numbers(cls, option_orders):
        results = []
        for oo in option_orders:
            keys_to_humanize = ["processed_premium"]
            coef = (1.0 if oo["direction"] == "credit" else -1.0)
            for k in keys_to_humanize:
                if oo[k] == None:
                    continue
                oo[k] = float(oo[k]) * coef
            results.append(oo)
        return results
