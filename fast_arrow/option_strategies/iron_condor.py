import numpy as np
import pandas as pd
import datetime


class IronCondor(object):

    @classmethod
    def sort_by_strike_price(cls, options):
        return sorted(options, key = (lambda x: x['strike_price']))

    @classmethod
    def gen_leg(cls, option_url, side="sell", position_effect=1, ratio_quantity=1):
        return {
            "side": side,
            "option": option_url,
            "position_effect": position_effect,
            "ratio_quantity": ratio_quantity
        }


    @classmethod
    def custom_generator_idea_one(cls, options,
        width, put_inner_lte_delta, call_inner_lte_delta):
        """
        totally just playing around ideas for the API.

        this IC sells
        - credit put spread
        - credit call spread

        the approach
        - set width for the wing spread (eg, 1, ie, 1 unit width spread)
        - set delta for inner leg of the put credit spread (eg, 0.2)
        - set delta for inner leg of the call credit spread (eg, 0.1)
        """

        #
        # put credit spread
        #
        put_options_unsorted = list(filter(lambda x: x['type'] == 'put', options))
        put_options = cls.sort_by_strike_price(put_options_unsorted)

        # @TODO this could be optimized, but it works
        deltas_as_strings = [x['delta'] for x in put_options]
        x = np.array(deltas_as_strings)
        deltas = x.astype(np.float)
        put_inner_index = np.argmin(deltas >= -put_inner_lte_delta) - 1
        put_outer_index = put_inner_index - width

        put_inner_leg = cls.gen_leg(put_options[put_inner_index]["instrument"])
        put_outer_leg = cls.gen_leg(put_options[put_outer_index]["instrument"])


        #
        # call credit spread
        #
        call_options_unsorted = list(filter(lambda x: x['type'] == 'call', options))
        call_options = cls.sort_by_strike_price(call_options_unsorted)

        # @TODO this could be optimized, but it works
        deltas_as_strings = [x['delta'] for x in call_options]
        x = np.array(deltas_as_strings)
        deltas = x.astype(np.float)
        call_inner_index = np.argmax(deltas < call_inner_lte_delta)
        call_outer_index = call_inner_index + width

        call_inner_leg = cls.gen_leg(call_options[call_inner_index]["instrument"])
        call_outer_leg = cls.gen_leg(call_options[call_outer_index]["instrument"])

        legs = [put_outer_leg, put_inner_leg,
            call_inner_leg, call_outer_leg]

        #
        # @TODO
        # calculate price
        # provide helper method to determine cumulative bid/ask spread
        #
        price = 100.0

        return legs,price
