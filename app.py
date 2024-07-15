from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__)

def scrape_with_selenium(symbol):
    try:
        # Setup the Chrome WebDriver with options
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-plugins')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        # Define the URL
        url = f'https://ticker.finology.in/company/{symbol}'

        # Open the webpage
        driver.get(url)

        # Use explicit wait for the elements to be present
        wait = WebDriverWait(driver, 10)

        # Define the CSS selectors for the required divs
        selectors = [
            'div#mainContent_ProsAndCons',
            'div#mainContent_updAddRatios',
            'div#mainContent_pricesummary',
            'div#mainContent_clsprice'
        ]

        scraped_data = {}

        for selector in selectors:
            elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector)))

            # Extract and store text content
            data = [element.text.strip() for element in elements]
            scraped_data[selector] = data

        # Close the browser
        driver.quit()

        return scraped_data

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

@app.route('/scrape', methods=['POST'])
def scrape_endpoint():
    symbol = request.json.get('symbol')
    if not symbol:
        return jsonify({'error': 'Symbol not provided'}), 400

    data = scrape_with_selenium(symbol)
    if data:
        return jsonify(data), 200
    else:
        return jsonify({'error': 'Failed to scrape data'}), 500

if __name__ == '__main__':
    # Run Flask app with Gunicorn server
    app.run(host='0.0.0.0', port=5000)
