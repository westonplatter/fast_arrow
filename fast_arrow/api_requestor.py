import requests


def gen_headers(token, bearer):
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en;q=1, fr;q=0.9, de;q=0.8, ja;q=0.7, nl;q=0.6, it;q=0.5",
        "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
        "X-Robinhood-API-Version": "1.0.0",
        "Connection": "keep-alive",
        "User-Agent": "Robinhood/823 (iPhone; iOS 7.1.2; Scale/2.00)"
    }
    if token:
        headers["Authorization"] = "Token {0}".format(token)
    if bearer:
        headers["Authorization"] = "Bearer {0}".format(bearer)
    return headers


def get(url, token=None, bearer=None, params={}):
    """
    Execute HTTP GET
    """
    headers = gen_headers(token, bearer)
    res = requests.get(url, headers=headers, params=params, timeout=15)
    return res.json()


def post(url, token=None, bearer=None, payload=None):
    """
    Execute HTTP POST
    """
    headers = gen_headers(token, bearer)
    res = requests.post(url, headers=headers, data=payload, timeout=15)
    return res.json()
