from fast_arrow.api_requestor import get


class Option(object):

    @classmethod
    def fetch(cls, bearer, id, insight=None):
        """
        fetch instrument
        """
        url = "https://api.robinhood.com/options/instruments/{0}/".format(id, insight)
        if insight:
            url = url + insight + "/"
        return get(url, bearer=bearer)
