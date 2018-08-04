from fast_arrow.api_requestor import get
from fast_arrow import util
from fast_arrow.resources.option import Option


class OptionPosition(object):

    @classmethod
    def all(cls, token):
        """
        fetch all option positions
        """
        url = 'https://api.robinhood.com/options/positions/'
        data = get(url, token=token)
        results = data["results"]
        while data["next"]:
            data = get(data["next"], token)
            results.extend(data["results"])
        return results


    @classmethod
    def append_marketdata(cls, bearer, option_positions):
        """
        Fetch and merge in Market Data for each option position
        """
        results = []
        for option_position in option_positions:
            id = util.get_last_path(option_position["option"])
            md = Option.marketdata(bearer, id)
            merged_dict = dict(list(option_position.items()) + list(md.items()))
            results.append(merged_dict)
        return results


    @classmethod
    def append_marketdata_list(cls, bearer, option_positions):
        """
        Fetch and merge in Market Data for each option position
        """
        ids = []
        for option_position in option_positions:
            _id = util.get_last_path(option_position["option"])
            ids.append(_id)

        mds = Option.marketdata_list(bearer, ids)

        results = []
        for op in option_positions:
            # @TODO how do I not make this O(n^2)?
            md = [md for md in mds if md['instrument'] == op['option']][0]
            merged_dict = (dict(list(op.items()) + list(md.items() )))
            results.append(merged_dict)

        return results
