import configparser
from urllib.parse import urlparse
import datetime


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


def days_ago(days):
    """
    Returns datetime object
    """
    return datetime.date.today() - datetime.timedelta(days=days)


def format_datetime(dt):
    """
    Returns ISO 8601 string representation
    """
    return dt.isoformat()


def is_max_date_gt(max_date, date):
    if max_date is None:
        return False
    if date < max_date:
        return True
    else:
        return False
