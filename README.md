# fast_arrow
A simple yet robust API client for Robinhood

[![Build Status](https://travis-ci.com/westonplatter/fast_arrow.svg?branch=master)](https://travis-ci.com/westonplatter/fast_arrow)
&nbsp;
[![Coverage
Status](https://coveralls.io/repos/github/westonplatter/fast_arrow/badge.svg?branch=master)](https://coveralls.io/github/westonplatter/fast_arrow?branch=master)
&nbsp;
[![Version](https://img.shields.io/pypi/v/fast_arrow.svg)](https://pypi.org/project/fast-arrow/)

## NOTE - changes coming with version >= 1.0

Sometime during Spring 2019, Robinhood changed how their API handles
authentication. In order to adapt to those changes, I've moved
"authentication" outside this library to `fast_arrow_auth`,
https://github.com/westonplatter/fast_arrow_auth.

Please see:
- [issue 35](https://github.com/westonplatter/fast_arrow/issues/85) for a
detailed account of the issue
- [this comment](https://github.com/westonplatter/fast_arrow/issues/85#issuecomment-513834267) for the approach I've taken to remediate auth issues
- [this PR](https://github.com/westonplatter/fast_arrow/pull/94) for a run down on exact code changes

I will be releasing these changes under version 1.0.0 to follow semantic
version guidelines (since auth changes are incompatible API changes).


## example

```py
from fast_arrow import Client, Stock, OptionChain, Option

#
# new auth process as of 1.0.0.rc1
# get auth_data (see https://github.com/westonplatter/fast_arrow_auth)
#
with open("fast_arrow_auth.json") as f:
    auth_data = json.loads(f.read())

#
# initialize client with auth_data
#
client = Client(auth_data)

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

## design principles

You might be asking, "yet another Robinhood client? There's already a few out
there. What's different about this one?"

`fast_arrow` holds to these __design principles__,  
- focus on simple features that expose data. Don't interpret data.  
- make __stock__ & __option__ operations easy to talk about and do with code  
- organize code in small and discrete python classes  
- use [fast_arrow_auth](https://github.com/westonplatter/fast_arrow_auth) to handle authentication process

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
- [x] fetch historical value of portfolio ([example](examples/portfolio_historicals.py))

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

### releases

Adding so I don't forget the next time I release a version,
```
python setup.py sdist bdist_wheel
twine upload dist/*
```

## projects using `fast_arrow`

- **simple_portfolio**. Export trades from Robinhood and run basic reporting on portfolio performance. https://github.com/westonplatter/simple_portfolio

- **chesterton**. A delightful little UI & trading bot for strategies on Robinhood. https://github.com/westonplatter/chesterton
