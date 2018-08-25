import requests



# def gen_headers(bearer):
#     headers = {
#         "Accept": "*/*",
#         "Accept-Encoding": "gzip, deflate",
#         "Accept-Language": "en;q=1, fr;q=0.9, de;q=0.8, ja;q=0.7, nl;q=0.6, it;q=0.5",
#         "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
#     }
#     if bearer:
#         headers["Authorization"] = "Bearer {0}".format(bearer)
#     return headers
#
#
# def get(url=None, client=None, params={}):
#     """
#     Execute HTTP GET
#     """
#     bearer = (client.access_token if client else None)
#     headers = gen_headers(bearer)
#     res = requests.get(url, headers=headers, params=params, timeout=15)
#     return res.json()
#
#
# def post(url=None, client=None, payload=None):
#     """
#     Execute HTTP POST
#     """
#     bearer = (client.access_token if client else None)
#     headers = gen_headers(bearer)
#     res = requests.post(url, headers=headers, data=payload, timeout=15)
#     return res.json()
