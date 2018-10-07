import numpy as np
import pandas as pd
import datetime
from decimal import Decimal


class IronCondor(object):

    @classmethod
    def sort_by_strike_price(cls, options):
        return sorted(options, key = (lambda x: x['strike_price']))


    @classmethod
    def gen_leg(cls, option_url, side, position_effect="open", ratio_quantity=1):
        assert side in ["buy", "sell"]
        assert position_effect in ["open", "close"]
        return {
            "side": side,
            "option": option_url,
            "position_effect": position_effect,
            "ratio_quantity": ratio_quantity
        }


    @classmethod
    def max_bid_ask_spread(cls, ic_options):
        max_spread = Decimal(0.0)
        for x in ic_options:
            ask = Decimal(x["ask_price"])
            bid = Decimal(x["bid_price"])
            spread = ask - bid
            if spread > max_spread:
                max_spread = spread
        return float(max_spread)


    @classmethod
    def strings_to_np_array(cls, strings):
        x = np.array(strings)
        deltas = x.astype(np.float)
        return np.nan_to_num(deltas)


    @classmethod
    def generate_by_deltas(cls, options,
        width, put_inner_lte_delta, call_inner_lte_delta):
        """
        totally just playing around ideas for the API.

        this IC sells
        - credit put spread
        - credit call spread

        the approach
        - set width for the wing spread (eg, 1, ie, 1 unit width spread)
        - set delta for inner leg of the put credit spread (eg, -0.2)
        - set delta for inner leg of the call credit spread (eg, 0.1)
        """

        #
        # put credit spread
        #
        put_options_unsorted = list(filter(lambda x: x['type'] == 'put', options))
        put_options = cls.sort_by_strike_price(put_options_unsorted)

        deltas_as_strings = [x['delta'] for x in put_options]
        deltas = cls.strings_to_np_array(deltas_as_strings)

        put_inner_index = np.argmin(deltas >= put_inner_lte_delta) - 1
        put_outer_index = put_inner_index - width

        put_inner_leg = cls.gen_leg(put_options[put_inner_index]["instrument"], "sell")
        put_outer_leg = cls.gen_leg(put_options[put_outer_index]["instrument"], "buy")


        #
        # call credit spread
        #
        call_options_unsorted = list(filter(lambda x: x['type'] == 'call', options))
        call_options = cls.sort_by_strike_price(call_options_unsorted)

        deltas_as_strings = [x['delta'] for x in call_options]
        x = np.array(deltas_as_strings)
        deltas = x.astype(np.float)
        # because deep ITM call options have a delta that comes up as NaN,
        # but are approximately 0.99 or 1.0, I'm replacing Nan with 1.0
        # so np.argmax is able to walk up the index until it finds "call_inner_lte_delta"
        # @TODO change this so (put credit / call credit) spreads work the same
        where_are_NaNs = np.isnan(deltas)
        deltas[where_are_NaNs] = 1.0

        call_inner_index = np.argmax(deltas <= call_inner_lte_delta)
        call_outer_index = call_inner_index + width

        call_inner_leg = cls.gen_leg(call_options[call_inner_index]["instrument"], "sell")
        call_outer_leg = cls.gen_leg(call_options[call_outer_index]["instrument"], "buy")

        legs = [put_outer_leg, put_inner_leg, call_inner_leg, call_outer_leg]

        #
        # price calcs
        #
        price = (
            -Decimal(put_options[put_outer_index]['adjusted_mark_price'])
            +Decimal(put_options[put_inner_index]['adjusted_mark_price'])
            +Decimal(call_options[call_inner_index]['adjusted_mark_price'])
            -Decimal(call_options[call_outer_index]['adjusted_mark_price'])
        )

        #
        # provide max bid ask spread diff
        #
        ic_options = [
            put_options[put_outer_index],
            put_options[put_inner_index],
            call_options[call_inner_index],
            call_options[call_outer_index]
        ]

        max_bid_ask_spread = cls.max_bid_ask_spread(ic_options)

        return {"legs": legs, "price": price,
            "max_bid_ask_spread": max_bid_ask_spread}
