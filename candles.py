#!/usr/bin/python

import json, hmac, hashlib, time, requests
import base64, datetime
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


api_url = 'https://api.gdax.com/'
API_KEY = ''
API_SECRET = ''
API_PASS = ''
auth = CoinbaseExchangeAuth(API_KEY, API_SECRET, API_PASS)

#last 5 trading days
diff = datetime.timedelta(days=5)
end = datetime.date.today()
start = end - diff
start_iso = str(start.isoformat())
end_iso = str(end.isoformat())
#60 = minute
#300 = 5 minutes
#900 = 15 minutes
#3600 = 1 hour
#21600 = 6 hours
#86400 = 1 day
granularity = str(3600)  # daily
# Get candles
query = 'start='+start_iso+'&end='+end_iso+'&granularity='+granularity
r = requests.get(api_url + '/products/BTC-USD/candles?'+query, auth=auth)
print(json.dumps(r.json(), indent=4, sort_keys=True))
