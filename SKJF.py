import requests
from bs4 import BeautifulSoup

def fetch_stock_price(symbol):
    url = f'https://ticker.finology.in/company/{symbol}'  # Replace with the actual URL pattern
    try:
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extracting stock price
            price_element = soup.find('span', id='mainContent_ltrlDebt')
            if price_element:
                price = price_element.text.strip()
            else:
                price = 'Price data not found'

            # Extracting price fluctuation
            fluctuation_element = soup.find('div', id='mainContent_updAddRatios')
            if fluctuation_element:
                fluctuation = fluctuation_element.text.strip()
            else:
                fluctuation = 'Fluctuation data not found'

            return {"success": True, "price": price, "fluctuation": fluctuation}

        else:
            return {"success": False, "message": f"Failed to retrieve data. Status code: {response.status_code}"}

    except requests.exceptions.RequestException as e:
        return {"success": False, "message": f"Error fetching data: {str(e)}"}

# Example usage:
symbol = 'ALKALI'  # Replace with the stock symbol you want to fetch
response = fetch_stock_price(symbol)
print(response)
