import numpy as np
import pandas as pd
import datetime

class IronCondor(object):

    @classmethod
    def custom_generator_idea_one(cls, options,
        width, put_inner_lte_delta,
        call_inner_lte_delta):
        """
        totally just playing around ideas for the API.

        this IC sells
        - credit put spread
        - credit call spread

        the approach
        - set width for the wing spread (eg, 1.0. ie a $100 notional)
        - set delta for inner leg of the put credit spread (eg, 0.2)
        - set delta for inner leg of the call credit spread (eg, 0.1)
        """

        import pdb; pdb.set_trace()

        put_options = list(filter(lambda x: x['type'] == 'put', options))

        call_options = list(filter(lambda x: x['type'] == 'call', options))

        legs = []
