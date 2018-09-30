import configparser
from fast_arrow import (
    Client,
    Option,
    OptionChain,
    OptionOrder,
    SpreadsVertical,
    Stock
)
import math


#
# get the authentication configs
#
config_file = "config.debug.ini"
config = configparser.ConfigParser()
config.read(config_file)
username = config['account']['username']
password = config['account']['password']


#
# initialize and authenticate Client
#
client = Client(username=username, password=password)
client.authenticate()

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
# enrich options with market data
#
ops = Option.mergein_marketdata_list(client, ops)

#
# genrate vertical spread table
#
width = 1
df = SpreadsVertical.gen_df(ops, width, "put", "sell")

#
# select the 4th row (should be a deep OTM put, credit spread)
#
vertical = df.iloc[[4]]

#
# create the order
#
direction = "credit"

legs = [
    {   "side": "sell",
        "option": vertical["instrument"].values[0],
        "position_effect": "open",
        "ratio_quantity": 1
    },
    {   "side": "buy",
        "option": vertical["instrument_shifted"].values[0],
        "position_effect": "open",
        "ratio_quantity": 1
    }
]

#
# for a Put Credit spread, set limit price at 1.0 less the full margin
#
my_bid_price = (vertical["margin"] * 100.0) - 1.00
my_bid_price_rounded = (math.floor(my_bid_price * 100.0))/100.0
x = my_bid_price_rounded / 100.0
my_bid_price_formatted = str(x)
price = my_bid_price_formatted

quantity = 1
time_in_force = "gfd"
trigger = "immediate"
order_type = "limit"

# @TODO create intuitive print statement
# print("Buying the {} {} {} for {} (dollar cost = ${})".format(
#     symbol,
#     strike_price,
#     desired_type,
#     my_bid_price_rounded,
#     my_bid_price_rounded*100.0)
# )

oo = OptionOrder.submit(client, direction, legs, price, quantity, time_in_force, trigger, order_type)

print("Order submitted ... ref_id = {}".format(oo["ref_id"]))

#
# cancel the order
#
print("Canceling order = {}".format(oo["ref_id"]))
result = OptionOrder.cancel(client, oo['cancel_url'])
print("Order canceled result = {}".format(result))
