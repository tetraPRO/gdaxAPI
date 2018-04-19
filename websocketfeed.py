import gdax, time, json

class myWebsocketClient(gdax.WebsocketClient):
    def on_open(self):
        self.url = "wss://ws-feed.gdax.com/"
        self.products = ["BTC-USD"]
        print("Connected to server!")

    def on_message(self, msg):
        if msg['type'] == 'match':
            if 'price' in msg:
                print("***LAST TRADE*** @ {:.2f}".format(float(msg["price"])))

    def on_close(self):
        print("-- Goodbye! --")

wsClient = myWebsocketClient()
wsClient.start()