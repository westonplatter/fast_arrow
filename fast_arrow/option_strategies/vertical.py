# @todo update dependencies
import numpy as np
import pandas as pd
import datetime

class Vertical(object):

    # def __init__(self, **kwargs):
    #     # self.fn     = kwargs.pop("fn", None)
    #     self.symbol = kwargs.pop("symbol", None)
    #     self.kind   = kwargs.pop("kind", None)
    #     self.width  = kwargs.pop("width", None)
    #     self.dte    = kwargs.pop("dte", None)
    #     self.__load_data()


    # def __repr__(self):
    #     return "<Spread symbol={} kind={} width={} dte={}>".format(self.symbol,
    #         self.kind, self.width, self.dte)


    # def __load_data(self):
    #     fn = "data/{}.json".format(self.symbol.upper())
    #     if self.fn == "help":
    #         fn = "../data/{}.json".format(self.symbol.upper())
    #
    #     self.df = pd.read_json(fn, orient="records")
    #     self.df['expiration_date'] = pd.to_datetime(self.df['expiration_date'], format="%Y-%m-%d")


    @classmethod
    def fetch_options_for_symbol(cls, symbol):
        return []


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
