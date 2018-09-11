import configparser
from fast_arrow import (
    Client,
    Option,
    OptionChain,
    OptionOrder,
    Stock,
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

desired_type = "call"
strike_price = math.floor(float(stock["ask_price"]) + 1.0)

ops = Option.mergein_marketdata_list(client, ops)

option_to_buy = None

for op in ops:
    if (float(op["strike_price"]) == strike_price) and (op["type"] == desired_type):
        option_to_buy = op



#
# send order
#
direction = "debit"

legs = [{ "side": "buy",
    "option": option_to_buy["url"],
    "position_effect": "open",
    "ratio_quantity": 1 }]

price = str(float(option_to_buy["bid_price"]))
quantity = 1
time_in_force = "gfd"
trigger = "immediate"
order_type = "limit"

oo = OptionOrder.submit(client, direction, legs, price, quantity, time_in_force, trigger, order_type)

#
# cancel order
#
OptionOrder.cancel(client, oo['cancel_url'])
