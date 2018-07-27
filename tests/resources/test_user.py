from fast_arrow import util
from fast_arrow.resources.auth import Auth
from fast_arrow.resources.user import User
from tests.test_util import gen_vcr


class TestUser(object):
    def test_fetch(self):
        token = '123'
        with gen_vcr().use_cassette('user_fetch.yaml'):
            data = User.fetch(token)
            assert(data['username'] == 'my_username')
