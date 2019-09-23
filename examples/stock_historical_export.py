import configparser
import json
import csv
from fast_arrow import (
    Client,
    StockMarketdata
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
symbol = "AAPL"
span = "week"
bounds = "regular"
data = StockMarketdata.historical_quote_by_symbol(client, symbol, span, bounds)

if len(data["historicals"]) > 0:
    csv_columns = data["historicals"][0].keys()
    filename = "examples/data_{}.csv".format(symbol)
    with open(filename, 'w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=csv_columns)
        writer.writeheader()
        for rec in data["historicals"]:
            writer.writerow(rec)
