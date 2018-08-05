from fast_arrow.api_requestor import get
from fast_arrow import util
from fast_arrow.resources.option import Option


class OptionPosition(object):

    @classmethod
    def all(cls, token, nonzero=False):
        """
        fetch all option positions
        """
        url = 'https://api.robinhood.com/options/positions/'
        params = {
            "nonzero": nonzero
        }
        data = get(url, token=token, params=params)
        results = data["results"]
        while data["next"]:
            data = get(data["next"], token)
            results.extend(data["results"])
        return results


    @classmethod
    def append_marketdata(cls, bearer, option_position):
        """
        Fetch and merge in Market Data for each option position
        """
        return cls.append_marketdata_list(bearer, [option_position])[0]


    @classmethod
    def append_marketdata_list(cls, bearer, option_positions):
        """
        Fetch and merge in Market Data for each option position
        """
        ids = cls._extract_ids(option_positions)
        mds = Option.marketdata_list(bearer, ids)
        results = []
        for op in option_positions:
            # @TODO optimize this so it's not O(n^2)
            md = [x for x in mds if x['instrument'] == op['option']][0]
            # there is no overlap in keys so this is fine
            merged_dict = dict( list(op.items()) + list(md.items()) )
            results.append(merged_dict)
        return results


    @classmethod
    def append_instrumentdata_list(cls, bearer, option_positions):
        ids = cls._extract_ids(option_positions)
        idatas = Option.fetch_list(bearer, ids)

        results = []
        for op in option_positions:
            idata = [x for x in idatas if x['url'] == op['instrument']][0]
            # there is an overlap in keys, {'chain_symbol', 'url', 'type', 'created_at', 'id', 'updated_at', 'chain_id'}
            # @TODO this is ugly. let's fix it later
            # alternative method,
            #   wanted_keys = ['strike_price']
            #   idata_subset = dict((k, idata[k]) for k in wanted_keys if k in idata)
            merge_me = {
                "option_type": idata["type"],
                "strike_price": idata["strike_price"],
                "expiration_date": idata["expiration_date"],
                "min_ticks": idata["min_ticks"]
            }
            merged_dict = dict( list(op.items()) + list(merge_me.items()) )
            results.append(merged_dict)

        return results


    @classmethod
    def humanize_numbers(cls, option_positions):
        results = []
        for op in option_positions:
            keys_to_humanize = [
                "delta",
                "theta",
                "gamma",
                "vega",
                "rho",
                "implied_volatility"]

            coef = (1.0 if op["type"] == "long" else -1.0)

            for k in keys_to_humanize:
                if op[k] == None:
                    continue
                op[k] = float(op[k]) * coef

            op["chance_of_profit"] = (op["chance_of_profit_long"] if op["type"] == "long" else op["chance_of_profit_short"])

            results.append(op)

        return results


    @classmethod
    def _extract_ids(cls, option_position):
        ids = []
        for op in option_position:
            _id = util.get_last_path(op["option"])
            ids.append(_id)
        return ids
