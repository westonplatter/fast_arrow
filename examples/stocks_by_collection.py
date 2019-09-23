import configparser
import json
from fast_arrow import (
    Client,
    Collection
)


print("----- running {}".format(__file__))


#
# get auth_data (see https://github.com/westonplatter/fast_arrow_auth)
#
with open("fast_arrow_auth.json") as f:
    auth_data = json.loads(f.read())


#
# initialize client with auth_data
#
client = Client(auth_data)

#
# fetch stocks (instruments) related to tag
#
tag = "China"
stocks = Collection.fetch_instruments_by_tag(client, tag)

#
# results
#
print("Found {} stocks related to {}".format(len(stocks), tag))
