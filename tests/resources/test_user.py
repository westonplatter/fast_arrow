from fast_arrow import util
from fast_arrow.resources.auth import Auth
from fast_arrow.resources.user import User
import vcr

favcr = vcr.VCR(
    cassette_library_dir='tests/fixtures_vcr',
    record_mode='none',
    match_on=['method', 'scheme', 'host', 'port', 'path', 'query'],
)

class TestUser(object):
    def get_token(self):
        username, password = util.get_username_password('config.test.ini')
        return Auth.login(username, password)

    def test_fetch(self):
        token = '123'
        with favcr.use_cassette('user_fetch.yaml'):
            resj = User.fetch(token)
            assert( resj['username'] == 'my_username')
