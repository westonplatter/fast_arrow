import configparser
import csv
from fast_arrow import (
    Client,
    StockMarketdata
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

def print_symbol_price(marketdata):
    msg = "Symbol = {}. Ask price = {}. Bid price = {}".format(
        marketdata['symbol'], marketdata['ask_price'], marketdata['bid_price'])
    print(msg)


#
# fetch by single stock symbol
#
symbol = "AAPL"
md = StockMarketdata.quote_by_symbol(client, symbol)
print_symbol_price(md)

#
# fetch by multiple stock symbols
#
symbols = ['AAPL', 'MU', 'FB']
mds = StockMarketdata.quote_by_symbols(client, symbols)
for md in mds:
    print_symbol_price(md)

#
# fetch by single 'instrument_id'
#
symbol = 'AAPL'
md = StockMarketdata.quote_by_symbol(client, symbol)
instrument_id = md['instrument'].split('/')[4]
md = StockMarketdata.quote_by_instrument(client, instrument_id)
print_symbol_price(md)

#
# fetch by multiple 'instrument_id's
#
symbols = ['AAPL', 'MU', 'FB']
mds = StockMarketdata.quote_by_symbols(client, symbols)
instrument_ids = [md['instrument'].split('/')[4] for md in mds]
mds = StockMarketdata.quote_by_instruments(client, instrument_ids)
for md in mds:
    print_symbol_price(md)
