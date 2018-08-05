import configparser
from fast_arrow.resources.auth import Auth
from fast_arrow.resources.option_chain import OptionChain
from fast_arrow.resources.option import Option
from fast_arrow.resources.option_position import OptionPosition

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
# fetch option_positions
#
all_option_positions = OptionPosition.all(token)


#
# filter to get open option_positions
#
open_option_positions = list(filter(lambda p: float(p["quantity"]) > 0.0, all_option_positions))


#
# append marketdata to each position
#
bearer = Auth.get_oauth_token(token)
option_position_with_marketdata = OptionPosition.append_marketdata_list(bearer, open_option_positions)


#
# append instrument data to each position
#
option_position_with_marketdata_and_instrument_data = OptionPosition.append_instrumentdata_list(bearer, option_position_with_marketdata)
