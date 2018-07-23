import hmac
import io
import logging
import sys
import os
import re

import configparser

FAST_ARROW_LOG = os.environ.get('FAST_ARROW_LOG')

logger = logging.getLogger('fast_arrow')

__all__ = [
    'io',
    'parse_qsl',
    'utf8',
    'log_info',
    'log_debug',
    'dashboard_link',
    'logfmt',
]

def convert_to_fa_object(resp):

    if isinstance(resp, dict):
        return dict

    if isinstance(resp, list):
        return [convert_to_fa_object(i) for i in resp]

def get_username_password(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    return [config['account']['username'], config['account']['password']]
