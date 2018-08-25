import unittest

from fast_arrow import util
from fast_arrow import OptionPosition
from tests.test_util import gen_vcr


class TestOptionPosition(unittest.TestCase):

    @unittest.skip("fix me")
    def test_fetch_fields(self):
        token = '123'
        with gen_vcr().use_cassette('option_position_all.yaml'):
            option_positions = OptionPosition.all(token)
            option_position = option_positions[0]

            expected_fields = [
                'intraday_average_open_price', 'account', 'intraday_quantity',
                'option', 'created_at', 'updated_at', 'average_price',
                'chain_id', 'pending_expired_quantity', 'pending_buy_quantity',
                'url', 'pending_sell_quantity', 'chain_symbol', 'type', 'id',
                'quantity']

            actual_fields = list(option_position.keys())

            assert(set(expected_fields) == set(actual_fields))
