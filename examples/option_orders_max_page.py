import configparser
import json
from fast_arrow import Client, OptionOrder
from datetime import datetime, timedelta


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
# fetch option orders for last 14 days
#
recent_orders = OptionOrder.all(client, max_fetches=3)

print(len(recent_orders))
