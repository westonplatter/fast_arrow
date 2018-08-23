import pandas as pd
import json
import configparser
from fast_arrow import (
    OptionChain,
    Option,
    OptionPosition,
    OptionMarketdata,
)
from fast_arrow.client import Client

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
client = Client(username, password)
client.client.authenticate()


#
# fetch option_positions
#
all_option_positions = OptionPosition.all(client)


#
# filter to get open option_positions
#
ops = list(filter(lambda p: float(p["quantity"]) > 0.0, all_option_positions))


#
# append marketdata to each position
#
ops = OptionPosition.mergein_marketdata_list(client, ops)



#
# append instrument data to each position
#
ops = OptionPosition.mergein_instrumentdata_list(client, ops)


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


#
# create Pandas DF of option positions
#
df = pd.DataFrame.from_dict(ops)
