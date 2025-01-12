from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__)

def scrape_with_selenium(symbol):
    try:
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')  # Disable GPU usage for headless mode stability
        options.add_argument('--no-sandbox')   # Required when running as root user
        options.add_argument('--disable-extensions')  # Disable loading of extensions
        options.add_argument('--disable-plugins')     # Disable loading of plugins
        options.add_argument('--enable-logging')
        options.add_argument('--v=1')


        # Configure WebDriver with ChromeDriverManager
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


        # Define the URL
        url = f'https://ticker.finology.in/company/{symbol}'

        # Open the webpage
        driver.get(url)

        # Use explicit waits for elements to load
        wait = WebDriverWait(driver, 10)

        # Define CSS selectors for required divs
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

        # Close the WebDriver
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
