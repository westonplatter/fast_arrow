from fast_arrow.resources.option_chain import OptionChain
from tests.test_util import gen_vcr, gen_client
import unittest


class TestPosition(object):

    def test_fetch_fields(self):
        client = gen_client()

        oc_id = "644f21f0-a166-4c94-bd67-02568d3a5940"
        oc_symbol = "TLT"

        with gen_vcr().use_cassette('option_chain_fetch.yaml'):
            chain = OptionChain.fetch(client, oc_id, oc_symbol)

            expected_fields = [
                'can_open_position', 'symbol', 'trade_value_multiplier',
                'underlying_instruments', 'expiration_dates', 'cash_component',
                'min_ticks', 'id']

            actual_fields = list(chain.keys())

            assert(set(expected_fields) == set(actual_fields))
