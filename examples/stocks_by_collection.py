import configparser
from fast_arrow import (
    Client,
    Collection
)


print("----- running {}".format(__file__))


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
client = Client(username=username, password=password)
client.authenticate()

#
# fetch stocks (instruments) related to tag
#
tag = "China"
stocks = Collection.fetch_instruments_by_tag(client, tag)

#
# results
#
print("Found {} stocks related to {}".format(len(stocks), tag))
