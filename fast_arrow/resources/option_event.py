from fast_arrow import util
from fast_arrow.resources.option import Option


class OptionEvent(object):

    @classmethod
    def all(cls, client):
        """
        fetch all option positions
        """
        url = 'https://api.robinhood.com/options/events/'
        params = { }
        data = client.get(url, params=params)
        results = data["results"]
        while data["next"]:
            data = get(data["next"], token)
            results.extend(data["results"])
        return results


    @classmethod
    def mergein_instrumentdata_list(cls, client, option_events):
        results = []
        ids = [util.get_last_path(oe['option']) for oe in option_events]
        idatas = Option.fetch_by_ids(client, ids)
        for oe in option_events:
            idata = [x for x in idatas if x['url'] == oe['option']][0]
            merge_me = {
                "option_type": idata["type"],
                "symbol": idata["chain_symbol"]
            }
            merged_dict = dict( list(oe.items()) + list(merge_me.items()) )
            results.append(merged_dict)
        return results


    @classmethod
    def humanize_numbers(cls, option_events):
        results = []
        for oe in option_events:
            keys_to_humanize = ["total_cash_amount"]

            coef = 0.0
            if oe["type"] == "exercise":
                coef = 1.0
            elif oe["type"] == "assignment":
                coef = -1.0

            for k in keys_to_humanize:
                if oe[k] == None:
                    continue
                oe[k] = float(oe[k]) * (coef)
            results.append(oe)

        return results
