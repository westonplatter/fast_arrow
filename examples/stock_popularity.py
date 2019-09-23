import configparser
import json
from fast_arrow import (
    Client,
    StockMarketdata,
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
# fetch option_positions
#
symbols = ["AAPL", "SQ", "USO"]

for symbol in symbols:
    md = StockMarketdata.quote_by_symbol(client, symbol)
    stock_id = md["instrument"].split("/")[-2]
    data = Stock.popularity(client, [stock_id])[0]
    num_open_positions = data["num_open_positions"]
    print(f"{symbol} has {num_open_positions} open positions")
