from binance.client import Client
import json

class BinanceP2PAPI:
    def __init__(self, api_key, api_secret):
        self.client = Client(api_key, api_secret)
    
    def get_currencies_and_payment_methods(self):
        ads = self.client.p2p.get_all_advertisements()
        currencies = {}
        for ad in ads:
            if ad['currency'] not in currencies:
                currencies[ad['currency']] = []
            for payment_method in ad['paymentMethods']:
                if payment_method not in currencies[ad['currency']]:
                    currencies[ad['currency']].append(payment_method)
        return currencies
    
    def write_to_file(self, data, filename):
        with open(filename, 'w') as outfile:
            json.dump(data, outfile)