import configparser
from fast_arrow import (
    Auth,
    OptionEvent
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
bearer = Auth.login_oauth2(username, password)


#
# fetch all option events
#
events = OptionEvent.all(bearer)
