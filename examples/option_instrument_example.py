import configparser
from fast_arrow import (
    Auth,
    OptionMarketdata
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
# get the bearer token
#
bearer = Auth.login_oauth2(username, password)


#
# get historical data for option id
#
_id = "5c56f5f1-d406-444c-bdfe-dbbdc19ced81"
span = "year"
interval = "day"

historical_data = OptionMarketdata.historicals_for_id(bearer, _id, span=span, interval=interval)
