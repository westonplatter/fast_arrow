from fast_arrow import util
from fast_arrow.resources.option import Option


class OptionOrder(object):

    @classmethod
    def all(cls, client):
        """
        fetch all option positions
        """
        url = 'https://api.robinhood.com/options/orders/'
        data = client.get(url)
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


    @classmethod
    def submit(cls, client, direction, legs, price, quantity, time_in_force, trigger, order_type, run_validations=True):
        '''
        params:
        - client
        - direction
        - legs
        - price
        - quantity
        - time_in_force
        - trigger
        - order_type
        - run_validations. default = True
        '''

        if run_validations:
            assert(direction in ["debit", "credit"])

            # @TODO - research this.
            # might be formatted as decimal w/ 1/100th percision. eg, 1.23
            assert(type(price) is str)

            assert(type(quantity) is int)
            assert(time_in_force in ["gfd", "gtc"])
            assert(trigger in ["immediate"])
            assert(order_type in ["limit", "market"])
            assert(cls._validate_legs(legs) is True)

        payload = {
            "account": client.account_url,
            "direction": direction,
            "legs": legs,
            "price": price,
            "quantity": quantity,
            "time_in_force": time_in_force,
            "trigger": trigger,
            "type": order_type,
        }
        request_url = "https://api.robinhood.com/options/orders/"
        data = client.post(request_url, payload=payload)
        return data


    @classmethod
    def _validate_legs(legs):
        for leg in legs:
            assert("option" in leg)
            assert(leg["position_effect"] in ["open", "close"])

            # @TODO research required formatting
            # assert(leg["ratio_quantity"])

            assert(leg["side"] in ["buy", "sell"])
        return True


    @classmethod
    def cancel(cls, client, cancel_url):
        result = client.post(cancel_url)
        if result is None:
            return True
        else:
            return False
