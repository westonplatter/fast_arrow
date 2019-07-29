import configparser
from fast_arrow import Client
from fast_arrow import Portfolio
from fast_arrow import Account


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
