import configparser
from fast_arrow import (
    Client,
    Option,
    OptionChain,
    OptionOrder,
    Stock,
)
import math

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
stock = Stock.mergein_marketdata_list(client, [stock])[0]

oc = OptionChain.fetch(client, stock["id"], symbol)
ed = oc['expiration_dates'][3]
ops = Option.in_chain(client, oc["id"], expiration_dates=[ed])

#
# select the $SPY calls
#
desired_type = "call"
ops = list(filter(lambda x: x["type"] == desired_type, ops))


#
# select a single $SPY call option
#
strike_price = math.floor(float(stock["ask_price"]) + 3.0)
strike_price_str = "{:.4f}".format(strike_price)
option_to_buy = None
# for op in ops:
#     if op["strike_price"] == strike_price_str:
#         option_to_buy = op
option_to_buy = ops[25]


#
# enrich selected option with market data
#
option_to_buy = Option.mergein_marketdata_list(client, [option_to_buy])[0]


#
# send order
# NOTE!!! (at 10% of market bid prices so we don't actually get filled)
#
direction = "debit"

legs = [{ "side": "buy",
    "option": option_to_buy["url"],
    "position_effect": "open",
    "ratio_quantity": 1 }]

if (float(option_to_buy["bid_price"]) * 0.1) > 0.01:
    my_bid_price = (float(option_to_buy["bid_price"]) * 0.1)
else:
    my_bid_price = 0.01

my_bid_price_rounded = (math.floor(my_bid_price * 100.0))/100.0
my_bid_price_formatted = str(my_bid_price_rounded)
price = my_bid_price_formatted

quantity = 1
time_in_force = "gfd"
trigger = "immediate"
order_type = "limit"

print("Buying the {} {} {} for {} (dollar cost = ${})".format(symbol,
    strike_price, desired_type, my_bid_price_rounded,
    my_bid_price_rounded*100.0)
)

oo = OptionOrder.submit(client, direction, legs, price, quantity, time_in_force, trigger, order_type)

print("Order submitted ... ref_id = {}".format(oo["ref_id"]))


#
# cancel the order
#
print("Canceling order = {}".format(oo["ref_id"]))
result = OptionOrder.cancel(client, oo['cancel_url'])
print("Order canceled result = {}".format(result))
