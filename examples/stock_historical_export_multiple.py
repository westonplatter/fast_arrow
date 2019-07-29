import configparser
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
symbols = ["AAPL", "MU"]
span = "week"
bounds = "regular"
data = StockMarketdata.historical_quote_by_symbols(
    client, symbols, span, bounds)

if len(data) > 0:
    filename = "examples/data_{}.csv".format("_".join(symbols))
    csv_columns = ['open_price', 'high_price', 'low_price', 'close_price']
    num_rows = len(data[0]['historicals'])

    with open(filename, 'w') as csv_file:
        writer = csv.writer(csv_file)

        headers = ['begins_at']
        for sym in symbols:
            for col in csv_columns:
                headers.append('{}_{}'.format(sym, col))
        writer.writerow(headers)

        for index in range(0, num_rows):
            row = []
            begins_at = data[0]['historicals'][index]['begins_at']
            row.append(begins_at)
            for ii, sym in enumerate(symbols):
                for col in csv_columns:
                    value = data[ii]['historicals'][index][col]
                    row.append(value)
            writer.writerow(row)
