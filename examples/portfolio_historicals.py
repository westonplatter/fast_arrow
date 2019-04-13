import configparser
from fast_arrow import Client
from fast_arrow import Portfolio
from fast_arrow import Account


print("----- running {}".format(__file__))


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


account = Account.all(client)[0]
account_number  = account['account_number']


span="year"
bounds="regular"
portfolio_historicals = Portfolio.historical(client, account_number, span, bounds)


ehs = portfolio_historicals["equity_historicals"]
begins_at = ehs[-1]["begins_at"]
ends_at = ehs[0]["begins_at"]


print(ehs[0].keys())
print("Fetched portfolio data between {} and {}".format(begins_at, ends_at))
