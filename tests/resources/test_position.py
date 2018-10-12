from fast_arrow import StockPosition
from tests.test_util import gen_vcr, gen_client

import unittest

class TestPosition(object):

    def test_fetch_fields(self):
        client = gen_client()
        with gen_vcr().use_cassette('position_all.yaml'):
            stock_positions = StockPosition.all(client)
            stock_position = stock_positions[0]

            expected_fields = [
                'shares_held_for_stock_grants', 'account',
                'pending_average_buy_price', 'shares_held_for_options_events',
                'intraday_average_buy_price', 'url',
                'shares_held_for_options_collateral', 'created_at',
                'updated_at','shares_held_for_buys', 'average_buy_price',
                'instrument','intraday_quantity', 'shares_held_for_sells',
                'shares_pending_from_options_events', 'quantity']

            actual_fields = list(stock_position.keys())

            assert(set(expected_fields) == set(actual_fields))
