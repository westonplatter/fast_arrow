#
# @TODO this list
#
# here's the idea.
# - [x] create an instance of client
# - [x] pass in username/password
# - [x] authenticate, save bearer token and refresh token
# - [x] pass this to http_requestor for gets and posts
# - [ ] if we get a token expired issue, refresh and retry
# - [ ] adjust all resources to use client instead of token/bearer
#
#

from fast_arrow.resources.auth import Auth
from fast_arrow.exceptions import AuthenticationError
from fast_arrow.resources.user import User

class Client(object):

    def __init__(self, **kwargs):
        self.options = kwargs

    def authenticate(self):
        if "username" in self.options and "password" in self.options:
            res = Auth.login_oauth2(self.options["username"], self.options["password"])
            self.access_token = res["access_token"]
            self.refresh_token = res["refresh_token"]
            self.mfa_code = res["mfa_code"]
            self.scope = res["scope"]
            return True

        elif "access_token" in self.options and "refresh_token" in self.options:
            self.access_token = self.options["access_token"]
            self.refresh_token = self.options["refresh_token"]
            # if we get HTTP 403, catch and raise error
            user = User.fetch(self)
            return True

        else:
            raise AuthenticationError("FastArrow: did not provide auth credentials")
