import configparser
from fast_arrow import (
    Client,
    StockPosition
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
# initialize and authenticate Client
#
client = Client(username=username, password=password)
client.authenticate()


#
# fetch stock positions
#
all_stock_positions = StockPosition.all(client)


#
# filter to get open positions
#
open_positions = list(filter(lambda x: float(x["quantity"]) > 0.0, all_stock_positions))
