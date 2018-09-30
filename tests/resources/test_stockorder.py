from fast_arrow import util
from fast_arrow import StockOrder
from tests.test_util import gen_vcr, gen_client

import unittest

class TestStockOrder(object):

    def test_fetch_fields(self):
        client = gen_client()
        with gen_vcr().use_cassette('stockorder_all.yaml'):
            orders = StockOrder.all(client)
            order = orders[0]

            expected_fields = ['updated_at', 'ref_id', 'time_in_force',
                'fees', 'cancel', 'response_category',
                'id', 'cumulative_quantity', 'stop_price', 'reject_reason', 'instrument',
                'state', 'trigger', 'override_dtbp_checks', 'type',
                'last_transaction_at', 'price', 'executions', 'extended_hours',
                'account', 'url', 'created_at', 'side', 'override_day_trade_checks', 'position',
                'average_price', 'quantity']

            actual_fields = list(order.keys())

            assert(set(expected_fields) == set(actual_fields))
