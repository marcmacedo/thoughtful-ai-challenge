from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from config import CHROME_DRIVER_PATH

class WebDrvierManager:
    def __init__(self, headless=True):
        self.headless = headless
        self.driver = self._initialize_driver()

    
    def _initialize_driver(self):
        options = Options()
        options.page_load_strategy = 'eager'

        if self.headless:
            options.add_argument('--headless')
            options.add_argument('--window-size=1920x1080') # This line is necessary to locate some elements that are hidden when the screen size is small or headless | This is the solution I found to solve this problem
        

        service = Service(CHROME_DRIVER_PATH)
        driver = webdriver.Chrome(service=service, options=options)
        return driver
    
    def get_driver(self):
        return self.driver
    
    def quit_driver(self):
        self.driver.quit()

