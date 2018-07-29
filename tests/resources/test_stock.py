from fast_arrow import util
from fast_arrow.resources.stock import Stock
from tests.test_util import gen_vcr


class TestStock(object):

    def test_fetch_fields(self):
        bearer = "123"
        symbol = "TLT"
        with gen_vcr().use_cassette('stock_fetch.yaml'):
            stock = Stock.fetch(bearer, symbol)

            expected_fields = ['margin_initial_ratio', 'rhs_tradability', 'id',
                'market', 'simple_name', 'min_tick_size', 'maintenance_ratio',
                'tradability', 'state', 'type', 'tradeable', 'fundamentals',
                'quote', 'symbol', 'day_trade_ratio', 'name',
                'tradable_chain_id', 'splits', 'url', 'country',
                'bloomberg_unique', 'list_date']

            actual_fields = list(stock.keys())

            assert(set(expected_fields) == set(actual_fields))
