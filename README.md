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
- [ ] fetch historical data
- [x] fetch all stock trades
- [ ] submit orders
- [ ] fetch earning events (past and future)
- [ ] fetch company news articles
- [ ] fetch company fundamentals
- [ ] fetch popularity data

**Options**
- [x] fetch option quotes ([example](examples/option_chain.py))
- [x] fetch open option positions ([example](examples/option_positions.py))
- [x] fetch all option orders (filled, canceled, rejected)
- [x] fetch historical options data ([example](examples/historical_option_data.py))
- [x] fetch option events ([example](examples/option_events.py))
- [ ] generate option strategy orders
  - [x] single ([example](examples/option_order_place_single.py))
  - [x] verticals ([example](examples/option_order_place_vertical.py))
  - [x] iron condors ([example](examples/option_order_place_iron_condor.py))
  - [ ] calendars
  - [ ] diagonals
- [ ] generate humanized names for option strategies
- [x] submit order ([example](examples/option_order_place_single.py))
- [x] cancel order ([example](examples/option_order_place_single.py))
- [x] replace order ([example](examples/option_order_replace.py))

**Portfolio**
- [x] [fetch historical value of portfolio](examples/portfolio_historicals.py)

**Authentication/Security**
- [x] handle standard Login/Logout flow [example](examples/auth.py)
- [x] handle MFA token during login [example](examples/auth_mfa.py)
- [x] pin SSL certificate (see [this PR](https://github.com/westonplatter/fast_arrow/pull/35))
- [x] automatically refreshes oauth2

__Want to propose a feature?__ [Open a feature request](https://github.com/westonplatter/fast_arrow/issues/new/choose) or open a Pull Request.


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

## projects using `fast_arrow`

- **simple_portfolio**. Export trades from Robinhood and run basic reporting on portfolio performance. https://github.com/westonplatter/simple_portfolio

- **chesterton**. A delightful little UI & trading bot for strategies on Robinhood. https://github.com/westonplatter/chesterton
