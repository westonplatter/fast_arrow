import configparser
import json
from fast_arrow import Client, OptionOrder


print("----- running {}".format(__file__))


config = configparser.ConfigParser()
config.read('config.debug.ini')


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
# fetch option orders
#
option_orders_all = OptionOrder.all(client)

#
# in case you have lots, only use first 25
# (unroll process fetches contract data for each leg)
#
option_orders = option_orders_all[0:25]


#
# unroll option orders ... ie, break each option leg into its own row
# this is helpful when doing detailed P/L reporting
#
option_orders_unrolled = OptionOrder.unroll_option_legs(client, option_orders)

#
# let's print out the results
#
print(option_orders_unrolled[0].keys())
