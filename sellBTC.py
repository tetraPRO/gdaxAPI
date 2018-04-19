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

#live boolean for live trading or not
#size of BTC to sell
#price in USD to sell at
def sellNow(live, size, price):
    if live:
        #~~~~~~~~~LIVE~~ACCOUNT~~TRADING~~~~~~~~~~~~
        api_url = 'https://api.gdax.com/'
        API_KEY = 'fb73318ded0a04b9ab31011147c4624b'
        API_SECRET = 'g3bBiSYOKTx6iIIzyKD8Ko3ZbDYJXXb10MRgUGp5cbyRsujoQpaGTihpd/uC46u+otsu5rRzJgKzEUvraYrQ7A=='
        API_PASS = 'vw2rhs8895'
        auth = CoinbaseExchangeAuth(API_KEY, API_SECRET, API_PASS)

        # Place an order
        order = {
            'size': size,
            'price': price,
            'stop': 'loss',
            'stop_price': price,
            'side': 'sell',
            'product_id': 'BTC-USD',
        }
        r = requests.post(api_url + 'orders', json=order, auth=auth)
        if r.status_code != 200:
            #the request has an error
            print("Message Error ")
        else:
            print(json.dumps(r.json(), indent=4, sort_keys=True))
            print('**********************************')
            print('****  LIVE TRADE SUCCESSFUL!  ****')
            print('**********************************')
    else:
        api_url = 'https://api-public.sandbox.gdax.com/'
        key = 'cccb03f901fd214a05dc28db4a84d108'
        secret = '/Gg077926cm2RstkXcVwBVT18kdpwoK4xVS74Vm/BLkcuv8fZiHU0jyzmoy6eSYgC4hnKwQdtEMHcRpIHyunBQ=='
        passphrase = 'yhwq4kurmq'
        auth = CoinbaseExchangeAuth(key, secret, passphrase)

        # Place an order
        order = {
            'size': size,
            'price': price,
            'stop': 'loss',
            'stop_price': price,
            'side': 'sell',
            'product_id': 'BTC-USD',
        }
        r = requests.post(api_url + 'orders', json=order, auth=auth)
        if r.status_code != 200:
            print("Message Error "+json.dumps(r.json()))
        else:
            print(json.dumps(r.json(), indent=4, sort_keys=True))
            print('**********************************')
            print('****  SIM TRADE SUCCESSFUL!   ****')
            print('**********************************')



sellNow(True, .05, 8100.0)