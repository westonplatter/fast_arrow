import configparser
from fast_arrow.client import Client

#
# get the authentication configs
#
config_file = "config.debug.ini"
config = configparser.ConfigParser()
config.read(config_file)
username = config['account']['username']
password = config['account']['password']

client = Client(username=username, password=password)
result = client.authenticate()

print("Authenticated successfully = {}".format(result))
