from fast_arrow import util
from fast_arrow.resources.option import Option
from fast_arrow.resources.option_marketdata import OptionMarketdata
from fast_arrow.util import is_max_date_gt


class OptionPosition(object):

    @classmethod
    def all(cls, client, **kwargs):
        """
        fetch all option positions
        """
        max_date = kwargs['max_date'] if 'max_date' in kwargs else None
        max_fetches = \
            kwargs['max_fetches'] if 'max_fetches' in kwargs else None
        nonzero = kwargs.get('nonzero', False)

        url = 'https://api.robinhood.com/options/positions/'
        params = {'nonzero': nonzero}
        data = client.get(url, params=params)
        results = data["results"]

        if is_max_date_gt(max_date, results[-1]['updated_at'][0:10]):
            return results
        if max_fetches == 1:
            return results

        fetches = 1
        while data["next"]:
            fetches = fetches + 1
            data = client.get(data["next"])
            results.extend(data["results"])
            if is_max_date_gt(max_date, results[-1]['updated_at'][0:10]):
                return results
            if max_fetches and (fetches >= max_fetches):
                return results
        return results

    @classmethod
    def append_marketdata(cls, client, option_position):
        """
        Fetch and merge in Marketdata for option position
        """
        return cls.append_marketdata_list(client, [option_position])[0]

    @classmethod
    def mergein_marketdata_list(cls, client, option_positions):
        """
        Fetch and merge in Marketdata for each option position
        """
        ids = cls._extract_ids(option_positions)
        mds = OptionMarketdata.quotes_by_instrument_ids(client, ids)

        results = []
        for op in option_positions:
            # @TODO optimize this so it's better than O(n^2)
            md = [x for x in mds if x['instrument'] == op['option']][0]
            # there is no overlap in keys so this is fine
            merged_dict = dict(list(op.items()) + list(md.items()))
            results.append(merged_dict)
        return results

    @classmethod
    def mergein_instrumentdata_list(cls, client, option_positions):
        ids = cls._extract_ids(option_positions)
        idatas = Option.fetch_list(client, ids)

        results = []
        for op in option_positions:
            idata = [x for x in idatas if x['url'] == op['instrument']][0]
            # there is an overlap in keys,
            # {'chain_symbol', 'url', 'type', 'created_at', 'id',
            #    'updated_at', 'chain_id'}
            # @TODO this is ugly. let's fix it later
            # alternative method,
            #   wanted_keys = ['strike_price']
            #   idata_subset = \
            #       dict((k, idata[k]) for k in wanted_keys if k in idata)
            merge_me = {
                "option_type": idata["type"],
                "strike_price": idata["strike_price"],
                "expiration_date": idata["expiration_date"],
                "min_ticks": idata["min_ticks"]
            }
            merged_dict = dict(list(op.items()) + list(merge_me.items()))
            results.append(merged_dict)

        return results

    @classmethod
    def humanize_numbers(cls, option_positions):
        results = []
        for op in option_positions:
            keys_to_humanize = [
                "quantity",
                "delta",
                "theta",
                "gamma",
                "vega",
                "rho"]

            coef = (1.0 if op["type"] == "long" else -1.0)

            for k in keys_to_humanize:
                if op[k] is None:
                    continue
                op[k] = float(op[k]) * coef

            if op["type"] == "long":
                op["chance_of_profit"] = op["chance_of_profit_long"]
            else:
                op["chance_of_profit"] = op["chance_of_profit_short"]

            results.append(op)

        return results

    @classmethod
    def _extract_ids(cls, option_positions):
        ids = []
        for op in option_positions:
            _id = util.get_last_path(op["option"])
            ids.append(_id)
        return ids
