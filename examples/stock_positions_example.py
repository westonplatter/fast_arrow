import configparser
# from fast_arrow.resources.auth import Auth
# from fast_arrow.resources.option_chain import OptionChain
# from fast_arrow.resources.option import Option
# from fast_arrow.resources.option_position import OptionPosition

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
token = Auth.login(username, password)

#
# fetch stock positions
#
all_stock_positions = StockPosition.all(token)

#
# filter to get open positions
#
open_positions = list(filter(lambda x: float(x["quantity"]) > 0.0, all_stock_positions))
