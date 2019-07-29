import configparser
from fast_arrow import (
    Client,
    OptionChain,
    Option,
    OptionPosition
)

print("----- running {}".format(__file__))

#
# get auth_data (see https://github.com/westonplatter/fast_arrow_auth)
#
with open("fast_arrow_auth.json") as f:
    auth_data = json.loads(f.read())


#
# initialize client with auth_data
#
client = Client(auth_data)


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
