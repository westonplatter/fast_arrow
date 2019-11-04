import configparser
import json
from fast_arrow import (
    Client,
    StockMarketdata,
    OptionChain,
    Option,
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
# fetch the stock info for TLT
#
symbol = "TLT"
md = StockMarketdata.quote_by_symbol(client, symbol)


#
# get the TLT option chain info
#
stock_id = md["instrument"].split("/")[-2]
option_chain = OptionChain.fetch(client, stock_id, symbol)
option_chain_id = option_chain["id"]
expiration_dates = option_chain['expiration_dates']


#
# reduce the number of expiration dates we're interested in
#
exp_dates = expiration_dates[2:3]


#
# get all options on the TLT option chain
#
ops = Option.in_chain(client, option_chain_id, expiration_dates=exp_dates)


#
# merge in market data fro TLT option instruments
#
ops = Option.mergein_marketdata_list(client, ops)


#
# determine the At The Money (ATM) call option IV
# (need the current underlying's price)
#

# get the last_trade_price of TLT
md = StockMarketdata.quote_by_symbol(client, symbol)
price = float(md['last_trade_price'])

# filter for call options
call_ops = list(filter(lambda op: op["type"] == "call", ops))

# sort the call options
sorted(call_ops, key=lambda op: float(op['strike_price']))

# find the first strike_price beyond the current price
atm_call_option = None
for call_op in call_ops:
    strike_price = float(call_op['strike_price'])
    if price < strike_price:
        atm_call_option = call_op

# get the IV
atm_iv = float(atm_call_option['implied_volatility'])

# done!
print(f"For {symbol}, at the money Implied Volatility = {atm_iv}")
