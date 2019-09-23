import configparser
import json
import math

from fast_arrow import (
    Client,
    StockMarketdata,
    Option,
    OptionChain,
    OptionMarketdata
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
# get TLT options
#
symbol = "TLT"
md = StockMarketdata.quote_by_symbol(client, symbol)
stock_id = md["instrument"].split("/")[-2]
oc = OptionChain.fetch(client, stock_id, symbol)
oc_id = oc["id"]
next_2_eds = oc['expiration_dates'][0:1]
ops = Option.in_chain(client, oc_id, expiration_dates=next_2_eds)


#
# get TLT in the middle of the current TLT trading range
#
urls = [op["url"] for op in ops]
middle = math.floor(len(urls)/2)
diff = math.floor(len(urls) * 0.7)
lower_end = middle - diff
higher_end = middle + diff
urls_subset = urls[lower_end:higher_end]


#
# get historical data for TLT options
#
hd = OptionMarketdata.historical_quotes_by_urls(client, urls_subset, span="year")
