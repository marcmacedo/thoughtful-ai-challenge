import json, os, logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Loading project configs (probably will keep all configs fixed in code)
config_path = os.path.join('config', 'config.json')
with open(config_path) as config_file:
    config = json.load(config_file)

driver_path = config['chromedriver_path']

# Maybe I'll change this later
logging.basicConfig(
    filename=f'{config["logs_path"]}/app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


logging.info('Info logging test!!!')



service = Service(executable_path=driver_path)

chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(service=service, options=chrome_options)


driver.get('https://www.aljazeera.com')

try:
    # element = driver.find_element(By.TAG_NAME, 'h1')
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'h3')))
    print(element.text)
finally:
    print("deu certo!")
driver.quit()