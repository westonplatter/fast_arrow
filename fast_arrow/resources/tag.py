from fast_arrow.api_requestor import get


class Tag(object):

    @classmethod
    def fetch_instruments_by_tag(cls, bearer, tag):
        base_url = "https://api.robinhood.com/midlands/tags/tag/"
        url = "{}{}/".format(base_url, tag.lower())
        res = get(url, bearer=bearer)
        result = (res["instruments"] if "instruments" in res else [])
        return result
