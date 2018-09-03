class Portfolio(object):

    @classmethod
    def historical(cls, client, account="", span="year", bounds="regular"):
        possible_intervals = {
            "day": "5minute",
            "week": "10minute",
            "year": "day",
            "5year": "week" }
        assert span in possible_intervals.keys()
        interval = possible_intervals[span]
        assert bounds in ["regular", "trading"]

        base_request_url = "https://api.robinhood.com/portfolios/historicals/"
        request_url = "{}{}/".format(base_request_url, account)
        params = { "span": span, "interval": interval, "bounds": bounds }
        data = client.get(request_url, params=params)
        return data
