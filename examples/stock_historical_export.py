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
symbol = "AAPL"
data = StockMarketdata.historical(client, symbol)


if len(data["historicals"]) > 0:
    csv_columns = data["historicals"][0].keys()
    filename = "examples/data_{}.csv".format(symbol)
    with open(filename, 'w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=csv_columns)
        writer.writeheader()
        for rec in data["historicals"]:
            writer.writerow(rec)
