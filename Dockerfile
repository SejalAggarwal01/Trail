# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install dependencies and Chrome
RUN apt-get update && \
    apt-get install -y wget unzip gnupg2 && \
    rm -rf /var/lib/apt/lists/* && \
    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable && \
    apt-get clean && \
    wget -q -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/$(wget -q -O - https://chromedriver.storage.googleapis.com/LATEST_RELEASE)/chromedriver_linux64.zip && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
    rm /tmp/chromedriver.zip

# Install Flask, Selenium, WebDriver Manager, and Gunicorn
RUN pip install --no-cache-dir flask selenium webdriver-manager gunicorn

# Command to run the Flask application with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
