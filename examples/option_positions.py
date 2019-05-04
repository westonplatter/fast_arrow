import configparser
from fast_arrow import (
    Client,
    OptionChain,
    Option,
    OptionPosition
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
# fetch option_positions
#
all_option_positions = OptionPosition.all(client)


#
# filter to get open option_positions
#
open_option_positions = list(filter(lambda p: float(p["quantity"]) > 0.0, all_option_positions))


#
# append marketdata to each position
#
option_position_with_marketdata = OptionPosition.mergein_marketdata_list(client, open_option_positions)


#
# append instrument data to each position
#
ption_position_with_marketdata_and_instrument_data = OptionPosition.mergein_instrumentdata_list(client, option_position_with_marketdata)
