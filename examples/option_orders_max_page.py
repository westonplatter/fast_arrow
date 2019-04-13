import configparser
from fast_arrow import Client, OptionOrder
from datetime import datetime, timedelta


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
# fetch option orders for last 14 days
#
recent_orders = OptionOrder.all(client, max_fetches=3)

print(len(recent_orders))
