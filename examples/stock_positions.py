import configparser
from fast_arrow import (
    Client,
    StockPosition
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
# fetch stock positions
#
all_stock_positions = StockPosition.all(client)


#
# filter to get open positions
#
open_positions = list(filter(lambda x: float(x["quantity"]) > 0.0, all_stock_positions))
