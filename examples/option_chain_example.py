import configparser
from fast_arrow import (
    Auth,
    Stock,
    OptionChain,
    Option
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
token = Auth.login(username, password)
bearer = Auth.get_oauth_token(token)


#
# fetch the stock info for TLT
#
symbol = "TLT"
stock = Stock.fetch(bearer, symbol)


#
# get the TLT option chain info
#
stock_id = stock["id"]
option_chain = OptionChain.fetch(bearer, stock_id)
option_chain_id = option_chain["id"]
expiration_dates = option_chain['expiration_dates']

#
# reduce the number of expiration dates we're interested in
#
next_3_expiration_dates = expiration_dates[0:3]

#
# get all options on the TLT option chain
#
tlt_options = Option.all(bearer, option_chain_id, next_3_expiration_dates)
