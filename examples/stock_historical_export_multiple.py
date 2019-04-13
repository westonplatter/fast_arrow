import configparser
import csv
from fast_arrow import (
    Client,
    StockMarketdata
)


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
