from fast_arrow.resources.option import Option
from fast_arrow.exceptions import NotImplementedError, TradeExecutionError

import uuid
import json


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
            data = client.get(data["next"])
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
    def unroll_option_legs(cls, client, option_orders):
        '''
        unroll option orders like this,
        https://github.com/joshfraser/robinhood-to-csv/blob/master/csv-options-export.py
        '''

        #
        # @TODO write this with python threats to make concurrent HTTP requests
        #

        results = []

        for oo in option_orders:
            for index, leg in enumerate(oo['legs']):
                for execution in leg['executions']:
                    order = dict()

                    for k,v in oo.items():
                        if k not in ['legs', 'price', 'type', 'premium', 'processed_premium', 'response_category', 'cancel_url']:
                            order[k] = oo[k]

                    order['order_type'] = oo['type']

                    contract = client.get(leg['option'])
                    order['leg'] = index+1
                    order['symbol'] = contract['chain_symbol']
                    order['strike_price'] = contract['strike_price']
                    order['expiration_date'] = contract['expiration_date']
                    order['contract_type'] = contract['type']

                    for k,v in leg.items():
                        if k not in ['id', 'executions']:
                            order[k] = leg[k]

                    coef = (-1.0 if leg['side'] == 'buy' else 1.0)
                    order['price'] = float(execution['price']) * 100.0 * coef
                    order['execution_id'] = execution['id']

                    results.append(order)
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
            assert(type(price) is str)
            assert(type(quantity) is int)
            assert(time_in_force in ["gfd", "gtc"])
            assert(trigger in ["immediate"])
            assert(order_type in ["limit", "market"])
            assert(cls._validate_legs(legs) is True)

        payload = json.dumps({
            "account": client.account_url,
            "direction": direction,
            "legs": legs,
            "price": price,
            "quantity": quantity,
            "time_in_force": time_in_force,
            "trigger": trigger,
            "type": order_type,
            "override_day_trade_checks": False,
            "override_dtbp_checks": False,
            "ref_id": str(uuid.uuid4())
        })

        request_url = "https://api.robinhood.com/options/orders/"
        data = client.post(request_url, payload=payload)
        return data

    @classmethod
    def _validate_legs(cls, legs):
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
        if result == {}:
            return True
        else:
            return False


    @classmethod
    def replace(cls, client, option_order, new_price):
        result = cls.cancel(client, option_order["cancel_url"])
        if not result:
            msg = "OptionOrder.replace() did not cancel previous OptionOrder"
            raise TradeExecutionError(msg)

        payload = json.dumps({
            "account": client.account_url,
            "direction": option_order["direction"],
            "legs": option_order["legs"],
            "price": new_price,
            "quantity": option_order["quantity"],
            "time_in_force": option_order["time_in_force"],
            "trigger": option_order["trigger"],
            "type": option_order["type"],
            "override_day_trade_checks": False,
            "override_dtbp_checks": False,
            "ref_id": str(uuid.uuid4())
        })

        request_url = "https://api.robinhood.com/options/orders/"
        data = client.post(request_url, payload=payload)
        return data
