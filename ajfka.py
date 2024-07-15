import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

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

        # Record the start time
        start_time = time.time()

        # Open the webpage
        driver.get(url)

        # Use explicit wait for the element to be present
        wait = WebDriverWait(driver, 10)
        elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div#mainContent_updAddRatios')))

        # Record the end time
        end_time = time.time()

        # Calculate the load time
        load_time = end_time - start_time
        print(f"Page load time: {load_time:.2f} seconds")

        # Extract and print text content
        for element in elements:
            print(element.text.strip())

        # Close the browser
        driver.quit()

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
symbol = '20MICRONS'  # Replace with the desired symbol
scrape_with_selenium(symbol)
