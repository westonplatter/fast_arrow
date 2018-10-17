import configparser
from fast_arrow import (
    Client,
    Stock,
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
# login and get the bearer token
#
client = Client(username=username, password=password)
client.authenticate()

#
# fetch stocks (instruments) related to tag
#
symbol = "NFLX"
num_open_positions = Stock.fetch_popularity(client, symbol)

#
# results
#
print("Number of open positions = {}".format(num_open_positions))
