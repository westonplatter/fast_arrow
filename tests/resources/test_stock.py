from fast_arrow import Stock
from fast_arrow.exceptions import ApiDoesNotSupportError
from tests.test_util import gen_client

import unittest


class TestStock(unittest.TestCase):

    def test_fetch(self):
        client = gen_client()
        symbol = "TLT"
        with self.assertRaises(ApiDoesNotSupportError):
            Stock.fetch(client, symbol)

    def test_all(self):
        client = gen_client()
        symbols = ["TLT", "USO"]
        with self.assertRaises(ApiDoesNotSupportError):
            Stock.all(client, symbols)
