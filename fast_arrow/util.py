# import hmac
# import io
# import logging
# import sys
# import os
# import re

import configparser
from urllib.parse import urlparse

# FAST_ARROW_LOG = os.environ.get('FAST_ARROW_LOG')
#
# logger = logging.getLogger('fast_arrow')
#
# __all__ = [
#     'io',
#     'parse_qsl',
#     'utf8',
#     'log_info',
#     'log_debug',
#     'dashboard_link',
#     'logfmt',
# ]

def get_username_password(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    return [config['account']['username'], config['account']['password']]


def get_last_path(url_string):
    o = urlparse(url_string)
    paths = o.path.rsplit("/")
    return list(filter(None, paths))[-1]
