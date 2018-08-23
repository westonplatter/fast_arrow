import configparser
from fast_arrow import (
    Auth,
    Tag
)

#
# get the authentication configs
#
config_file = "config.debug.ini"
config = configparser.ConfigParser()
config.read(config_file)
username = config['account']['username']
password = config['account']['password']

#
# login and get the bearer token
#
bearer = Auth.login_oauth2(username, password)

#
# fetch stocks (instruments) related to tag
#
tag = "China"
stocks = Tag.fetch_instruments_by_tag(bearer, tag)

#
# results
#
print("Found {} stocks related to {}".format(len(stocks), tag))
