#!/usr/bin/python

import json, hmac, hashlib, time, requests, base64, sys
from requests.auth import AuthBase


# Create custom authentication for Exchange
class CoinbaseExchangeAuth(AuthBase):
    def __init__(self, api_key, secret_key, passphrase):
        self.api_key = api_key
        self.secret_key = secret_key
        self.passphrase = passphrase

    def __call__(self, request):
        timestamp = str(time.time())
        message = timestamp + request.method + request.path_url + (request.body or '')
        hmac_key = base64.b64decode(self.secret_key)
        signature = hmac.new(hmac_key, message, hashlib.sha256)
        signature_b64 = signature.digest().encode('base64').rstrip('\n')

        request.headers.update({
            'CB-ACCESS-SIGN': signature_b64,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-KEY': self.api_key,
            'CB-ACCESS-PASSPHRASE': self.passphrase,
            'Content-Type': 'application/json'
        })
        return request


# ~~~~~~~~~LIVE~~ACCOUNT~~TRADING~~~~~~~~~~~~
api_url = 'https://api.gdax.com/'
API_KEY = ''
API_SECRET = ''
API_PASS = ''
auth = CoinbaseExchangeAuth(API_KEY, API_SECRET, API_PASS)
r = requests.get(api_url+'products/BTC-USD/book?level=2', auth=auth)
print(json.dumps(r.json(), indent=4, sort_keys=True))
