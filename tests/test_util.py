import vcr

from fast_arrow import Client


def gen_vcr():
    return vcr.VCR(
        cassette_library_dir='tests/fixtures_vcr',
        record_mode='none',
        match_on=['method', 'scheme', 'host', 'port', 'path', 'query'],
    )


def gen_client():
    auth_data = gen_auth_data()
    client = Client(auth_data)
    return client


def gen_auth_data():
    auth_data = {
        "account_id": 123,
        "access_token": "123",
        "refresh_token": "xxx_refresh_token",
        "device_token": "eeced862-f819-4c51-ad8d-969ae2bb5ddf",
    }
    return auth_data
