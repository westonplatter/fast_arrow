import configparser
from fast_arrow import (
    Client,
    Stock,
    Option,
    OptionChain,
    OptionMarketdata
)

#
# get the authentication configs
#
config_file = "config.debug.ini"
config = configparser.ConfigParser()
config.read(config_file)
username = config['account']['username']
password = config['account']['password']

#
# instantiate and authetnicate client
#
client = Client(username=username, password=password)
client.authenticate()

#
# get TLT options
#
symbol = "TLT"
stock = Stock.fetch(client, symbol)

stock_id = stock["id"]
oc = OptionChain.fetch(client, stock_id, symbol)
oc_id = oc["id"]
next_2_eds = oc['expiration_dates'][0:1]
ops = Option.in_chain(client, oc_id, expiration_dates=next_2_eds)

#
# get TLT in the middle of the current TLT trading range
#
urls = [op["url"] for op in ops]
import math
middle = math.floor(len(urls)/2)
diff = math.floor(len(urls) * 0.7)
lower_end = middle - diff
higher_end = middle + diff
urls_subset = urls[lower_end:higher_end]

#
# get historical data for TLT options
#
hd = OptionMarketdata.historical_quotes_by_urls(client, urls_subset, span="year")
