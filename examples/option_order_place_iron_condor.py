import configparser
from fast_arrow import (
    Client,
    OptionOrder,
    IronCondor
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
# fetch spy options
#
symbol = "SPY"
stock = Stock.fetch(client, symbol)
stock = Stock.mergein_marketdata_list(client, [stock])[0]

oc = OptionChain.fetch(client, stock["id"], symbol)
ed = oc['expiration_dates'][10]
ops = Option.in_chain(client, oc["id"], expiration_dates=[ed])

#
# enrich options with market data
#
ops = Option.mergein_marketdata_list(client, ops)


#
# programmtically generate legs for IronCondor
#
width = 1
put_inner_lte_delta = 0.2
call_inner_lte_delta = 0.1
ic = IronCondor.custom_generator_idea_one(ops, width, put_inner_lte_delta, call_inner_lte_delta)
