from fast_arrow import Dividend
from tests.test_util import gen_vcr, gen_client

import unittest

class TestDividend(object):

    def test_fetch_fields(self):
        client = gen_client()
        with gen_vcr().use_cassette('dividend_all.yaml'):
            dividends = Dividend.all(client)
            dividend = dividends[0]

            expected_fields = ['account', 'url', 'amount',
                'payable_date', 'instrument', 'rate',
                'record_date', 'position', 'withholding', 'id', 'paid_at']

            actual_fields = list(dividend.keys())

            assert(set(expected_fields) == set(actual_fields))
