import configparser
from fast_arrow import Client, OptionOrder
from datetime import datetime, timedelta


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
# fetch option orders for last 14 days
#
past_date = (datetime.now() - timedelta(days=14)).strftime("%Y-%m-%d")
recent_orders = OptionOrder.all(client, max_date=past_date)

#
# unroll option orders ... ie, break each option leg into its own row
# this is helpful when doing detailed P/L reporting
#
unrolled_option_orders = OptionOrder.unroll_option_legs(client, recent_orders)


#
# let's print out the results
#
print(option_orders_unrolled[1:10])
