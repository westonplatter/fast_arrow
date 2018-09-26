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
    def gen_table(cls, options, width):
        return []

        # self.kind = (dd["kind"] if "kind" in dd else self.kind)
        # assert self.kind is not None

        # self.type = (dd["type"] if "type" in dd else self.type)
        # assert self.type is not None

        # self.width = (abs(dd["width"]) if "width" in dd else self.width)

        # self.dte = (dd["dte"] if "dte" in dd else self.dte)
        # assert self.dte is not None

        #     # create the resulting/specific df (sdf is in a row on the keyboard)
        #     self.sdf = self.df.sort_values(["expiration_date", "strike_price"])
        #
        #     #
        #     # filter by dte param
        #     #
        #     self.dte_min = (datetime.datetime.now() + datetime.timedelta(days=self.dte[0]))
        #     self.dte_max = (datetime.datetime.now() + datetime.timedelta(days=self.dte[1]))
        #     self.sdf = self.sdf[ self.df["expiration_date"] >= self.dte_min ]
        #     self.sdf = self.sdf[ self.df["expiration_date"] <= self.dte_max ]
        #
        #     self.sdf = self.sdf[self.sdf["type"] == self.type]
        #
        #     coef = (1 if self.kind == "sell" else -1)
        #
        #     for k,v in self.sdf.groupby("expiration_date"):
        #
        #         sps = np.sort(v.strike_price.values)
        #         shift = self._calc_shift(sps, self.width)
        #
        #         if shift is None:
        #             continue
        #
        #         shift = int(shift) * coef
        #         shiftdf = v.shift(shift)
        #
        #         v["strike_price_shifted"] = (shiftdf["strike_price"])
        #
        #         if self.kind == "sell":
        #             v["margin"] = (v["strike_price"] - shiftdf["strike_price"])
        #         else:
        #             v["margin"] = 0.0
        #
        #         v["premium"]        = (v["adjusted_mark_price"] - shiftdf["adjusted_mark_price"])
        #         v["delta_spread"]   = (v["delta"] - shiftdf["delta"])
        #         v["theta_spread"]   = (v["theta"] - shiftdf["theta"])
        #
        #         merge_cols = ["strike_price_shifted", "margin", "premium", "delta_spread", "theta_spread"]
        #
        #         for col in merge_cols:
        #             self.sdf.loc[v.index, col] = v[col]
        #
        #     return self.sdf
        #
        #
        # def _calc_shift(self, sps, width):
        #     '''
        #     calc spread step to achieve desird margin
        #     @todo clean this up
        #     '''
        #     total = len(sps)
        #     median = int(np.floor(total/2))
        #
        #     if np.allclose((abs(sps[median] - 0.50) % 1.0), 0.0):
        #         median += 1
        #
        #     min_tick = (sps[median] - sps[median-1]) * 100.0
        #     if (min_tick - self.width) > 0.0:
        #         return None
        #
        #     shift = 0
        #     diff = 1
        #     searching = True
        #     marign = 0
        #
        #     while searching:
        #         margin = (sps[median] - sps[median-diff]) * 100
        #         if np.allclose(margin, self.width):
        #             shift = diff
        #             searching = False
        #         diff += 1
        #
        #     return shift
