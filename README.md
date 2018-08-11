# fast_arrow
API client for Robinhood

[![Build Status](https://travis-ci.com/westonplatter/fast_arrow.svg?branch=master)](https://travis-ci.com/westonplatter/fast_arrow)
[![Coverage
Status](https://coveralls.io/repos/github/westonplatter/fast_arrow/badge.svg?branch=master)](https://coveralls.io/github/westonplatter/fast_arrow?branch=master)

<hr/>
WARNING. this project is under active development (pre alpha).
USE AT YOUR OWN RISK.
<hr/>


## install
pip install fast_arrow

## example
@todo

## philosophy
`fast_arrow` is Robinhood api client, not an automated trading system. thus, "keep it simple stupid"

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

Run the test suite against a specific python version,
```
pipenv run tox -e py36
```
