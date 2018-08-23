import configparser
from fast_arrow import (
    Auth,
    OptionEvent
)
from fast_arrow.client import Client


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
client = Client(username, password)
client.client.authenticate()


#
# fetch all option events
#
events = OptionEvent.all(client)
