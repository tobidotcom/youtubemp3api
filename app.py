from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import logging
import os

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def download_video(url):
    options = Options()
    options.headless = True
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('start-maximized')
    options.add_argument('disable-infobars')
    options.add_argument('--disable-extensions')
    options.add_argument('--proxy-server="direct://"')
    options.add_argument('--proxy-bypass-list=*')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')

    # Path to ChromeDriver; ensure it's included in your Heroku environment or use an alternative
    driver_path = '/app/.chromedriver/bin/chromedriver'
    driver = webdriver.Chrome(executable_path=driver_path, options=options)

    try:
        driver.get(url)
        time.sleep(10)  # Adjust as needed for page load time
        # Implement your video download logic here
    finally:
        driver.quit()

@app.route('/convert', methods=['POST'])
def convert_youtube_to_mp3():
    data = request.json
    url = data.get('url')

    if not url:
        return jsonify({'error': 'URL is required'}), 400

    try:
        download_video(url)
        return jsonify({'message': 'Conversion initiated successfully'}), 200
    except Exception as e:
        logger.error(f"Error: {e}")
        return jsonify({'error': 'An error occurred while processing the request.'}), 500

if __name__ == '__main__':
    app.run(debug=True)
