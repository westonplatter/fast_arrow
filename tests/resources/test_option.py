import unittest

from fast_arrow import util
from fast_arrow.resources.option import Option
from tests.test_util import gen_vcr


class TestOption(unittest.TestCase):

    def test_fetch_fields(self):
        bearer = "123"
        id = "e03e7414-527d-4b44-a081-c61aeb474060"
        with gen_vcr().use_cassette("option_fetch.yaml"):
            option = Option.fetch(bearer, id)

            expected_fields = [
                'issue_date', 'tradability', 'strike_price', 'state', 'url',
                'expiration_date', 'created_at', 'chain_id', 'updated_at',
                'rhs_tradability', 'type', 'chain_symbol', 'min_ticks', 'id']

            actual_fields = list(option.keys())

            assert(set(expected_fields) == set(actual_fields))

    @unittest.skip("fix me")
    def test_marketdata_fields(self):
        bearer = "123"
        id = "e03e7414-527d-4b44-a081-c61aeb474060"

        with gen_vcr().use_cassette("option_marketdata.yaml"):
            marketdata = Option.marketdata(bearer, id)

            expected_fields = [
                'adjusted_mark_price', 'ask_price', 'ask_size', 'bid_price',
                'bid_size', 'break_even_price', 'high_price', 'instrument',
                'last_trade_price', 'last_trade_size', 'low_price', 'mark_price',
                'open_interest', 'previous_close_date', 'previous_close_price',
                'volume', 'chance_of_profit_long', 'chance_of_profit_short',
                'delta', 'gamma', 'implied_volatility', 'rho', 'theta', 'vega']

            actual_fields = list(marketdata.keys())

            assert(set(expected_fields) == set(actual_fields))
