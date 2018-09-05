import configparser
from fast_arrow import (
    Client,
    OptionOrder
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
# initialize and authenticate Client
#
client = Client(username=username, password=password)
client.authenticate()


#
# configure order details
#
# @TODO
# - fetch spy options
# - find 0.8 delta debit call to buy in next 60 days
# - set price at 0.01
# - send order
# - cancel order
#
#
