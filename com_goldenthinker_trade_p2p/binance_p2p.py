import requests
import json
import argparse
import sys

# Constants
DEFAULT_BINANCE_P2P_URL = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/ads/list"
DEFAULT_PAYMENT_METHOD_URL = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/configuration/publishers"

HEADERS = {
    'User-Agent': 'Mozilla/5.0',
    'Content-Type': 'application/json',
    'Referer': 'https://p2p.binance.com/',
    # Add any additional headers if required
}

def get_fiat_currencies(binance_p2p_url):
    """
    Fetches all available FIAT currencies from Binance P2P.
    Returns:
        List of fiat currency codes.
    """
    payload = {
        "asset": "USDT",  # Assuming USDT as the base asset
        "countries": [],
        "page": 1,
        "payTypes": [],
        "publisherType": None,
        "rows": 1,  # Minimal data to fetch currencies
        "tradeType": "BUY",
        "transAmount": 0
    }
    
    try:
        response = requests.post(binance_p2p_url, headers=HEADERS, json=payload)
        if response.status_code != 200:
            print(f"Failed to fetch fiat currencies. Status Code: {response.status_code}")
            print(f"Response Content: {response.text}")
            sys.exit(1)
        
        data = response.json()
        fiat_currencies = set()
        for ad in data.get('data', []):
            fiat = ad.get('advertiser', {}).get('countryCode')
            if fiat:
                fiat_currencies.add(fiat)
        
        # If API does not provide, define a static list (as of 2023)
        if not fiat_currencies:
            fiat_currencies = [
                "USD", "EUR", "GBP", "BRL", "IDR", "TRY", "UAH", "RUB",
                "KRW", "VND", "MYR", "PHP", "PEN", "MXN", "NGN",
                "COP", "SAR", "AED", "BDT"
            ]
        
        return list(fiat_currencies)
    
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching fiat currencies: {e}")
        sys.exit(1)

def get_payment_methods(payment_method_url):
    """
    Fetches all available payment methods from Binance P2P.
    Returns:
        List of payment method strings.
    """
    try:
        response = requests.get(payment_method_url, headers=HEADERS)
        if response.status_code != 200:
            print(f"Failed to fetch payment methods. Status Code: {response.status_code}")
            print(f"Response Content: {response.text}")
            sys.exit(1)
        
        data = response.json()
        payment_methods = []
        for method in data.get('data', []):
            pay_method = method.get('paymentMethod', {}).get('identifier')
            if pay_method:
                payment_methods.append(pay_method)
        
        # If API does not provide, define a static list (as of 2023)
        if not payment_methods:
            payment_methods = [
                "bank_transfer", "paypal", "cash_deposit", "web_money",
                "neteller", "skrill", "western_union", "alipay",
                "wechat", "qiwi", "eps", "ideal", "przelewy24"
            ]
        
        return payment_methods
    
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching payment methods: {e}")
        sys.exit(1)

def get_p2p_orders(binance_p2p_url, operation, asset, fiat_currency, payment_methods, amount, sort_by):
    """
    Fetches P2P orders based on the provided parameters.
    
    Args:
        binance_p2p_url (str): API endpoint for fetching P2P ads.
        operation (str): 'BUY' or 'SELL'.
        asset (str): Asset symbol, e.g., 'USDT'.
        fiat_currency (str): FIAT currency code.
        payment_methods (list): List of payment method identifiers.
        amount (float): Transaction amount.
        sort_by (str): Sorting criteria.
    
    Returns:
        List of available P2P ads/orders.
    """
    sort_mapping = {
        "Price": "price_asc",  # Ascending price
        "Completed Order Number": "completed_orders_desc",
        "Completion Rate": "completion_rate_desc",
        "Rating": "rating_desc"
    }
    
    sort = sort_mapping.get(sort_by, "price_asc")
    
    page = 1
    orders = []
    
    while True:
        payload = {
            "asset": asset,
            "countries": [],  # Empty means all countries
            "page": page,
            "payTypes": payment_methods,
            "publisherType": None,
            "rows": 10,  # Number of ads per page
            "tradeType": operation,
            "transAmount": amount
        }
        
        try:
            response = requests.post(binance_p2p_url, headers=HEADERS, json=payload)
            if response.status_code != 200:
                print(f"Failed to fetch P2P orders. Status Code: {response.status_code}")
                print(f"Response Content: {response.text}")
                break
            
            data = response.json()
            ads = data.get('data', [])
            if not ads:
                break  # No more ads available
            
            for ad in ads:
                advertiser = ad.get('advertiser', {})
                order = {
                    "Advertiser": advertiser.get('nickName'),
                    "Trade Type": ad.get('tradeType'),
                    "Asset": ad.get('asset'),
                    "Fiat Currency": ad.get('fiatUnit'),
                    "Price": ad.get('price'),
                    "Min Single Transactable Amount": ad.get('minSingleTransacted'),
                    "Max Single Transactable Amount": ad.get('maxSingleTransacted'),
                    "Payment Method": ad.get('tradeMethods')[0].get('identifier') if ad.get('tradeMethods') else None,
                    "Order Count": advertiser.get('orderCount'),
                    "Completion Rate": advertiser.get('completionRate'),
                    "Rate Star": advertiser.get('rateStar')
                }
                orders.append(order)
            
            page += 1  # Move to the next page
        
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while fetching P2P orders: {e}")
            break
    
    return orders

def main():
    parser = argparse.ArgumentParser(description="Binance P2P Marketplace Script")
    
    parser.add_argument("--operation", type=str, required=True, choices=["BUY", "SELL"],
                        help="Operation type: BUY or SELL")
    parser.add_argument("--asset", type=str, default="USDT",
                        help="Asset symbol, e.g., USDT (default: USDT)")
    parser.add_argument("--amount", type=float, required=True,
                        help="Transaction amount")
    parser.add_argument("--fiat_currency", type=str, required=True,
                        help="FIAT currency code, e.g., USD")
    parser.add_argument("--payment_methods", type=str, nargs='+', required=True,
                        help="Payment method identifiers, e.g., bank_transfer paypal")
    parser.add_argument("--sort_by", type=str, required=True,
                        choices=["Price", "Completed Order Number", "Completion Rate", "Rating"],
                        help="Sort by criteria")
    parser.add_argument("--binance_p2p_url", type=str, default=DEFAULT_BINANCE_P2P_URL,
                        help="Binance P2P ads API endpoint")
    parser.add_argument("--payment_method_url", type=str, default=DEFAULT_PAYMENT_METHOD_URL,
                        help="Binance P2P payment methods API endpoint")
    
    # Additional arguments for debugging
    parser.add_argument("--list_fiats", action='store_true',
                        help="List available FIAT currencies")
    parser.add_argument("--list_payments", action='store_true',
                        help="List available payment methods")
    
    args = parser.parse_args()
    
    # Load FIAT currencies and payment methods
    p2p_fiat_currencies = get_fiat_currencies(args.binance_p2p_url)
    p2p_payment_methods = get_payment_methods(args.payment_method_url)
    
    if args.list_fiats:
        print("Available FIAT Currencies:")
        for fiat in p2p_fiat_currencies:
            print(f"- {fiat}")
        sys.exit(0)
    
    if args.list_payments:
        print("Available Payment Methods:")
        for method in p2p_payment_methods:
            print(f"- {method}")
        sys.exit(0)
    
    # Validate fiat currency
    if args.fiat_currency not in p2p_fiat_currencies:
        print(f"Invalid fiat currency. Available options are: {p2p_fiat_currencies}")
        sys.exit(1)
    
    # Validate payment methods
    invalid_methods = [method for method in args.payment_methods if method not in p2p_payment_methods]
    if invalid_methods:
        print(f"Invalid payment methods: {invalid_methods}. Available options are: {p2p_payment_methods}")
        sys.exit(1)
    
    # Fetch P2P orders
    orders = get_p2p_orders(
        binance_p2p_url=args.binance_p2p_url,
        operation=args.operation,
        asset=args.asset,
        fiat_currency=args.fiat_currency,
        payment_methods=args.payment_methods,
        amount=args.amount,
        sort_by=args.sort_by
    )
    
    if not orders:
        print("No available orders found with the given parameters.")
        sys.exit(0)
    
    # Display the orders
    print(f"\nAvailable P2P Orders for {args.operation} {args.asset} in {args.fiat_currency}:\n")
    for idx, order in enumerate(orders, start=1):
        print(f"Order #{idx}")
        print(f"  Advertiser: {order['Advertiser']}")
        print(f"  Trade Type: {order['Trade Type']}")
        print(f"  Asset: {order['Asset']}")
        print(f"  Fiat Currency: {order['Fiat Currency']}")
        print(f"  Price: {order['Price']}")
        print(f"  Min Amount: {order['Min Single Transactable Amount']}")
        print(f"  Max Amount: {order['Max Single Transactable Amount']}")
        print(f"  Payment Method: {order['Payment Method']}")
        print(f"  Order Count: {order['Order Count']}")
        print(f"  Completion Rate: {order['Completion Rate']}")
        print(f"  Rating: {order['Rate Star']}")
        print("-" * 40)

if __name__ == "__main__":
    main()
