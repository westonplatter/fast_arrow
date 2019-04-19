import vcr

from fast_arrow import Client


def gen_vcr():
    return vcr.VCR(
        cassette_library_dir='tests/fixtures_vcr',
        record_mode='none',
        match_on=['method', 'scheme', 'host', 'port', 'path', 'query'],
    )


def gen_client():
    return Client()
