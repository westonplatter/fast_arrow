class Tag(object):

    @classmethod
    def fetch_instruments_by_tag(cls, client, tag):
        base_url = "https://api.robinhood.com/midlands/tags/tag/"
        url = "{}{}/".format(base_url, tag.lower())
        res = client.get(url)
        result = (res["instruments"] if "instruments" in res else [])
        return result
