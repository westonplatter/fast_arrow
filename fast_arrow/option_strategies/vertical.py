import numpy as np
import pandas as pd
import datetime

class Vertical(object):

    @classmethod
    def gen_df(cls, options, width, spread_type="call", spread_kind="buy"):
        """
        Generate Pandas Dataframe of Vertical

        :param options: python dict of options.
        :param width: offset for spread. Must be integer.
        :param spread_type: call or put. defaults to "call".
        :param spread_kind: buy or sell. defaults to "buy".
        """
        assert type(width) is int
        assert spread_type in ["call", "put"]
        assert spread_kind in ["buy", "sell"]

        # get CALLs or PUTs
        options = list(filter(lambda x: x["type"] == spread_type, options))

        coef = (-1 if spread_kind == "buy" else 1)
        shift = (coef * width)

        df = pd.DataFrame.from_dict(options)
        df['expiration_date'] = pd.to_datetime(df['expiration_date'], format="%Y-%m-%d")
        df['adjusted_mark_price'] = pd.to_numeric(df['adjusted_mark_price'])
        df['strike_price'] = pd.to_numeric(df['strike_price'])

        df.sort_values(["expiration_date", "strike_price"], inplace=True)

        for k,v in df.groupby("expiration_date"):
            sdf = v.shift(shift)

            df.loc[v.index, "strike_price_shifted"] = sdf["strike_price"]
            df.loc[v.index, "instrument_shifted"] = sdf["instrument"]

            if spread_kind == "sell":
                df.loc[v.index, "margin"] = v["strike_price"] - sdf["strike_price"]
            else:
                df.loc[v.index, "margin"] = 0.0

            df.loc[v.index, "premium"] = (v["adjusted_mark_price"] - sdf["adjusted_mark_price"])

        return df
