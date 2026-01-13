from binance_p2p_api import BinanceP2PAPI

api_key = 'your_api_key'
api_secret = 'your_api_secret'

binance_p2p_api = BinanceP2PAPI(api_key, api_secret)

currencies = binance_p2p_api.get_currencies_and_payment_methods()
binance_p2p_api.write_to_file(currencies, 'currencies.json')