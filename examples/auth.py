import configparser
import json

from fast_arrow import Client
from fast_arrow.resources.user import User

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

print("Account Id = {}".format(client.account_id))

user = User.fetch(client)
print("Username = {}".format(user["username"]))

result = client.relogin_oauth2()
print("Re-Authenticated with refresh_token successfully = {}".format(result))

refreshed_auth_data = client.current_auth_data()
filename = "fast_arrow_auth.json"
with open(filename, "w") as f:
    f.write(json.dumps(refreshed_auth_data, indent=4))
