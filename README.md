# fast_arrow
A simple yet robust API client for Robinhood

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

Install the package from pypi,
```
pip install fast_arrow
```

## another Robinhood client?

`fast_arrow` at its core,
1) is a Robinhood api client focused on simple and robust features
2) provides first class support for *stock* and *option* trading
3) organizes code in small and discrete python classes


## features

Here's what you can do with `fast_arrow` (some features still in development)

**Stocks**
- [x] get quotes
- [x] fetch all stock trades
- [ ] fetch historical data
- [ ] submit orders

**Options**
- [x] [fetch option quotes](examples/option_chain_example)
- [x] [fetch open option positions](examples/option_positions_example.py)
- [x] fetch all option orders (filled, canceled, rejected)
- [x] [fetch historical options data](examples/historical_option_data_example.py)
- [x] [fetch option events](examples/option_event_example.py)
- [ ] generate various option orders
  - [x] [single](examples/option_order_place_single.py)
  - [ ] verticals
  - [ ] iron condors
  - [ ] calendars
  - [ ] diagonals
- [x] submit order
- [x] cancel order


**Portfolio**
- [x] [fetch historical value of portfolio](examples/portfolio_historicals.py)

**Authentication/Security**
- [x] pin SSL certificate (see [this PR](https://github.com/westonplatter/fast_arrow/pull/35))
- [x] implments oauth2 automatic refresh
- [ ] handle MFA token during login

__Want to propose a feature? Pull request changes to the readme.__


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
