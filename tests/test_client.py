import unittest

from fast_arrow import Client
from fast_arrow.exceptions import AuthDataError


class TestClient(unittest.TestCase):

    def example_auth_data(self):
        return {
            "account_id": "123abc",
            "access_token": "my_access_token",
            "refresh_token": "123abc_my_refresh_token",
            "device_token": "9c24bddb-1a28-4d21-b871-0166d1837077"
        }

    def test_init(self):
        auth_data = self.example_auth_data()
        Client(auth_data)

    def test_init_validates_auth_data(self):
        auth_data = self.example_auth_data()
        del auth_data['account_id']
        with self.assertRaises(AuthDataError):
            Client(auth_data)

    def test_current_auth_data(self):
        auth_data = self.example_auth_data()
        client = Client(auth_data)
        ad = client.current_auth_data()
        for key in auth_data.keys():
            assert(auth_data[key] == ad[key])
