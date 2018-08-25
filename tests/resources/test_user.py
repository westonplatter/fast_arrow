from fast_arrow import util
from fast_arrow import User
from tests.test_util import gen_vcr

import unittest

class TestUser(object):
    @unittest.skip("fix me")
    def test_fetch(self):
        token = '123'
        with gen_vcr().use_cassette('user_fetch.yaml'):
            data = User.fetch(token)
            assert(data['username'] == 'my_username')
