import datetime
import json

from fast_arrow import api_requestor, util

class FastArrowObject(dict):

    def __init__(self, id=None, api_key=None, **params):
        super(FastArrowObject, self).__init__()
        self.api_key = api_key

    def request(self, method, url, params=None):
        if params is None:
        requestor = api_requestor.ApiRequestor(
            key=self.api_key,
            api_base=self.api_base())
        response = requestor.request(method, url, params)

        return util.convert_to_fa_object(response)
