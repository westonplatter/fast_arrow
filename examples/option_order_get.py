import configparser
from fast_arrow import (
    Client,
    Option,
    OptionChain,
    OptionOrder,
    Vertical,
    Stock
)
import math


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
# fetch option order
#
# intentionally fake order id
order_id = '89f89cde-27a8-4175-b4a8-d19ee87d2eca'
option_order = OptionOrder.get(client, order_id)
