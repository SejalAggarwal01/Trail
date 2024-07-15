from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Ensure GUI is off for server-side operation

# Set up the WebDriver
webdriver_service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)

# IMDb URL for top movies
url = "https://www.imdb.com/chart/top/"
driver.get(url)

# Wait for the page to load
time.sleep(5)

# Scraping data using Selenium
movie_elements = driver.find_elements(By.XPATH, "//td[@class='titleColumn']/a")
rating_elements = driver.find_elements(By.XPATH, "//td[@class='ratingColumn imdbRating']/strong")

# Print the top 10 movies and their ratings
print("Top 10 Movies on IMDb:")
for i in range(10):
    movie_title = movie_elements[i].text
    movie_rating = rating_elements[i].text
    print(f"{i+1}. {movie_title} - Rating: {movie_rating}")

# Close the WebDriver
driver.quit()
