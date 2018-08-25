# fast_arrow
A robust yet simple API client for Robinhood.

[![Build Status](https://travis-ci.com/westonplatter/fast_arrow.svg?branch=master)](https://travis-ci.com/westonplatter/fast_arrow)
&nbsp;
[![Coverage
Status](https://coveralls.io/repos/github/westonplatter/fast_arrow/badge.svg?branch=master)](https://coveralls.io/github/westonplatter/fast_arrow?branch=master)
&nbsp;
[![Version](https://img.shields.io/pypi/v/fast_arrow.svg)](https://pypi.org/project/fast-arrow/)


## example

```py
from fast_arrow import Client, Stock, OptionChain, Option

#
# Oauth2 authenticate with Robinhood
#
client = Client(username=username, password=password)
client.authenticate()

#
# fetch the stock info for TLT
#
symbol = "TLT"
stock = Stock.fetch(client, symbol)

#
# get the TLT option chain
#
stock_id = stock["id"]
option_chain = OptionChain.fetch(client, stock_id)

#
# let's get TLT options (calls and puts) for next 4 expiration dates
#
oc_id = option_chain["id"]
eds = option_chain['expiration_dates'][0:3]

#
# get all options on the TLT option chain
#
ops = Option.in_chain(client, oc_id, expiration_dates=eds)

#
# merge in market data fro TLT option instruments (ask, bid, delta, theta, etc)
#
ops = Option.mergein_marketdata_list(client, ops)
```

## install
Install the package from pypi


```
pip install fast_arrow
```


## philosophy
`fast_arrow` is a Robinhood api client, not an automated trading system. Thus,
the goal is "keep it simple stupid".

Robinhood as an API has a few different core objects,
- instruments (Option, Stock)
- marketdata (OptionMarketdata, StockMarketdata)
- positions (OptionPosition, StockPosition)
- orders (OptionOrder, StockOrder)
- account stuff (that I'll build for later)

`fast_arrow` expects that users want to merge these core objects. For example,
fetch Apple, Inc (Stock) quote data (StockMarketdata) to display the current
price per share of $APPL stock.

## development
Install [pipenv](https://github.com/pypa/pipenv), and then run,
```
pipenv install --dev
```

Run the test suite via,
```
make test
```

Run all the examples (make sure you add username/password to config.debug.ini),
```
sh run_all_examples.sh
```

Run the test suite against a specific python version,
```
pipenv run tox -e py36
```
