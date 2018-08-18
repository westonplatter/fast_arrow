import configparser
from fast_arrow import (
    Auth,
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
# login and get the bearer token
#
bearer = Auth.login_oauth2(username, password)

#
# fetch stock positions
#
all_stock_positions = StockPosition.all(bearer)


#
# filter to get open positions
#
open_positions = list(filter(lambda x: float(x["quantity"]) > 0.0, all_stock_positions))
