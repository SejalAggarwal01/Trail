from nselib import capital_market

try:
    print("Testing API call...")
    data = capital_market.market_watch_all_indices()
    if data is None or 'last' not in data or 'indexSymbol' not in data:
        raise ValueError("Unexpected response format from API")
    print("API call successful. Data:", data)
except Exception as e:
    print("Error during API call:",e)