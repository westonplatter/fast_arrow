import configparser
from fast_arrow import Client, OptionOrder


print("----- running {}".format(__file__))


config = configparser.ConfigParser()
config.read('config.debug.ini')


#
# initialize fast_arrow client and authenticate
#
client = Client(
    username = config['account']['username'],
    password = config['account']['password'])

client.authenticate()


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
