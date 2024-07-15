import requests

url = 'http://127.0.0.1:5000/scrape'
data = {'symbol': 'AAPL'}
response = requests.post(url, json=data)

if response.status_code == 200:
    print(response.json())
else:
    print('Failed to scrape data:', response.status_code)
