#!/usr/bin/python
import json, hmac, hashlib, time, requests, base64
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


def orderStatus(live, order_id):
    if live:
        # ~~~~~~~~~LIVE~~ACCOUNT~~TRADING~~~~~~~~~~~~
        api_url = 'https://api.gdax.com/'
        API_KEY = 'fb73318ded0a04b9ab31011147c4624b'
        API_SECRET = 'g3bBiSYOKTx6iIIzyKD8Ko3ZbDYJXXb10MRgUGp5cbyRsujoQpaGTihpd/uC46u+otsu5rRzJgKzEUvraYrQ7A=='
        API_PASS = 'vw2rhs8895'
        auth = CoinbaseExchangeAuth(API_KEY, API_SECRET, API_PASS)
        r = requests.get(api_url+'orders/'+order_id, auth=auth)
        print(json.dumps(r.json(), indent=4, sort_keys=True))
    else:
        api_url = 'https://api-public.sandbox.gdax.com/'
        key = 'cccb03f901fd214a05dc28db4a84d108'
        secret = '/Gg077926cm2RstkXcVwBVT18kdpwoK4xVS74Vm/BLkcuv8fZiHU0jyzmoy6eSYgC4hnKwQdtEMHcRpIHyunBQ=='
        passphrase = 'yhwq4kurmq'
        auth = CoinbaseExchangeAuth(key, secret, passphrase)
        r = requests.get(api_url + 'orders/'+order_id, auth=auth)
        print(json.dumps(r.json(), indent=4, sort_keys=True))



orderStatus(False, 'cce31f21-3afa-443f-93b7-cd550100d324')