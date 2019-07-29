import pandas as pd
import json
import configparser
from fast_arrow import (
    Client,
    OptionChain,
    Option,
    OptionPosition,
    OptionMarketdata,
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
ops = list(filter(lambda p: float(p["quantity"]) > 0.0, all_option_positions))
#
msg = "There are {} open option positions".format(len(ops))
print(msg)


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
#
print(df)
