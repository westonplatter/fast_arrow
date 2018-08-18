import configparser
from fast_arrow import (
    Auth,
    OptionChain,
    Option,
    OptionPosition
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
# fetch option_positions
#
all_option_positions = OptionPosition.all(bearer)


#
# filter to get open option_positions
#
open_option_positions = list(filter(lambda p: float(p["quantity"]) > 0.0, all_option_positions))


#
# append marketdata to each position
#
option_position_with_marketdata = OptionPosition.mergein_marketdata_list(bearer, open_option_positions)


#
# append instrument data to each position
#
option_position_with_marketdata_and_instrument_data = OptionPosition.mergein_instrumentdata_list(bearer, option_position_with_marketdata)
