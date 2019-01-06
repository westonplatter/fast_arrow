from fast_arrow import (
    Client,
    StockMarketdata
)

#
# initialize. Don't need to authenticate for stock data.
#
client = Client()

#
# fetch price quote data
#
symbol = "SQ"
stock = StockMarketdata.quote_by_symbol(client, symbol)

print("{} ask_price = {}".format(stock['symbol'], stock['ask_price']))
print("{} bid_price = {}".format(stock['symbol'], stock['bid_price']))
