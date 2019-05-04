import configparser
from fast_arrow import (
    Client,
    Option,
    OptionChain,
    OptionOrder,
    Vertical,
    Stock
)
import math

print("----- running {}".format(__file__))

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
ed = oc['expiration_dates'][0]
ops = Option.in_chain(client, oc["id"], expiration_dates=[ed])

#
# enrich options with market data
#
ops = Option.mergein_marketdata_list(client, ops)

#
# genrate vertical spread table
#
width = 1
spread_type = "put"
spread_kind = "sell"
df = Vertical.gen_df(ops, width, spread_type, spread_kind)

#
# select the 4th row (should be a deep OTM put, credit spread)
#
index = int(len(ops) / 4)
vertical = df.iloc[[index]]

#
# create the order
#
direction = "credit"

legs = [
    {   "side": spread_kind,
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

print("Selling a {} {}/{} {} spread for {} (notation value = ${})".format(
    symbol,
    vertical["strike_price"].values[0],
    vertical["strike_price_shifted"].values[0],
    spread_type,
    price,
    my_bid_price_rounded)
)

oo = OptionOrder.submit(client, direction, legs, price, quantity, time_in_force, trigger, order_type)

print("Order submitted ... ref_id = {}".format(oo["ref_id"]))

#
# cancel the order
#
print("Canceling order = {}".format(oo["ref_id"]))
result = OptionOrder.cancel(client, oo['cancel_url'])
print("Order canceled result = {}".format(result))
