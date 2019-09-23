import configparser
import json
from fast_arrow import (
    Client,
    Option,
    OptionChain,
    OptionOrder,
    Vertical,
    Stock
)
import math

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
# fetch option order
#
# intentionally fake order id
order_id = '89f89cde-27a8-4175-b4a8-d19ee87d2eca'
option_order = OptionOrder.get(client, order_id)
