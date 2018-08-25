import configparser
from fast_arrow import Client
from fast_arrow.resources.user import User

#
# get the authentication configs
#
config_file = "config.debug.ini"
config = configparser.ConfigParser()
config.read(config_file)
username = config['account']['username']
password = config['account']['password']

client = Client(username=username, password=password)
result = client.authenticate()

print("Authenticated successfully = {}".format(result))

user = User.fetch(client)
print("Username = {}".format(user["username"]))

result = client.relogin_oauth2()
print("Re-Authenticated with refresh_token successfully = {}".format(result))

result = client.logout_oauth2()
print("Logged out successfully = {}".format(result))
