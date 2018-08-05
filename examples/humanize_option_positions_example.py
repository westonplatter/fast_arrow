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
token = Auth.login(username, password)


#
# fetch option_positions
#
all_option_positions = OptionPosition.all(token)


#
# filter to get open option_positions
#
ops = list(filter(lambda p: float(p["quantity"]) > 0.0, all_option_positions))


#
# append marketdata to each position
#
bearer = Auth.get_oauth_token(token)
ops = OptionPosition.append_marketdata_list(bearer, ops)


#
# append instrument data to each position
#
ops = OptionPosition.append_instrumentdata_list(bearer, ops)


#
# humanize_numbers, so that
#   - delta
#   - theta
#   - gamma
#   - vega
#   - rho
#   - implied_volatility
# are positive or negative based on Long/Short position type
#
# And also add column "chance_of_profit" specific to Long/Short position type
#
ops = OptionPosition.humanize_numbers(ops)
