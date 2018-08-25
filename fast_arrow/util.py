import configparser
from urllib.parse import urlparse


def get_username_password(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    return [config['account']['username'], config['account']['password']]


def get_last_path(url_string):
    o = urlparse(url_string)
    paths = o.path.rsplit("/")
    return list(filter(None, paths))[-1]


def chunked_list(_list, _chunk_size=50):
    """
    Break lists into small lists for processing:w
    """
    for i in range(0, len(_list), _chunk_size):
        yield _list[i:i + _chunk_size]
