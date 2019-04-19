from fast_arrow import User
from tests.test_util import gen_vcr, gen_client


class TestUser(object):
    def test_fetch(self):
        client = gen_client()
        with gen_vcr().use_cassette('user_fetch.yaml'):
            data = User.fetch(client)
            assert(data['username'] == 'my_username')
