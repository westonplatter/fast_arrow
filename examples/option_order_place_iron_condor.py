#
# IC example not functional as of the 0.3.0 release
# pull requests welcome!
#

import configparser
from fast_arrow import (
    Client,
    IronCondor,
    Option,
    OptionChain,
    OptionOrder,
    Stock
)

print("----- running {}".format(__file__))

#
# get auth_data (see https://github.com/westonplatter/fast_arrow_auth)
#
with open("fast_arrow_auth.json") as f:
    auth_data = json.loads(f.read())


#
# initialize client with auth_data
#
client = Client(auth_data)


#
# fetch spy options
#
symbol = "SPY"
stock = Stock.fetch(client, symbol)

oc = OptionChain.fetch(client, stock["id"], symbol)
ed = oc['expiration_dates'][10]
ops = Option.in_chain(client, oc["id"], expiration_dates=[ed])

#
# enrich options with market data
#
ops = Option.mergein_marketdata_list(client, ops)


#
# programmtically generate legs for IronCondor
#
width = 1
put_inner_lte_delta = -0.2
call_inner_lte_delta = 0.1
# ic = IronCondor.generate_by_deltas(ops,width, put_inner_lte_delta, call_inner_lte_delta)
#
# direction = "credit"
# legs = ic["legs"]
# # @TODO create helper methods to handle floating arith and rounding issues
# # for now, it works good enough
# price_notional = ic["price"] * 100
# price_notional_fourth = price_notional / 4
# price_order = price_notional_fourth / 100
# price = str(price_order)
#
# quantity = 1
# time_in_force = "gfd"
# trigger = "immediate"
# order_type = "limit"
#
# # @TODO create human description of IC
# # print("Selling a {} {}/{} Put Spread for {} (notional value = ${})".format(
# #     symbol,
# #     vertical["strike_price"].values[0],
# #     vertical["strike_price_shifted"].values[0],
# #     price,
# #     my_bid_price_rounded)
# # )
#
# oo = OptionOrder.submit(client, direction, legs, price, quantity, time_in_force, trigger, order_type)
#
# print("Order submitted ... ref_id = {}".format(oo["ref_id"]))
#
# #
# # cancel the order
# #
# print("Canceling order = {}".format(oo["ref_id"]))
# result = OptionOrder.cancel(client, oo['cancel_url'])
# print("Order canceled result = {}".format(result))
