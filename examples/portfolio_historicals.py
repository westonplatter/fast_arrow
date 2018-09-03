import configparser
from fast_arrow import Client
from fast_arrow import Portfolio

#
# get the authentication configs
#
config_file = "config.debug.ini"
config = configparser.ConfigParser()
config.read(config_file)
username = config['account']['username']
password = config['account']['password']
account  = config['account']['account']

client = Client(username=username, password=password)
result = client.authenticate()

span="year"
bounds="regular"
portfolio_historicals = Portfolio.historical(client, account, span, bounds)

ehs = portfolio_historicals["equity_historicals"]
begins_at = ehs[-1]["begins_at"]
ends_at = ehs[0]["begins_at"]

print(ehs[0].keys())

print("Fetched portfolio data between {} and {}".format(begins_at, ends_at))
