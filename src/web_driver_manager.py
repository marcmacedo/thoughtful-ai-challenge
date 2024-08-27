from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from config import CHROME_DRIVER_PATH
from logger import setup_logger

logger = setup_logger()



class WebDrvierManager:
    def __init__(self, headless=True):
        self.headless = headless
        self.driver = self._initialize_driver()

    
    def _initialize_driver(self):
        logger.info(f'Starting WebDriver on mode headless={self.headless}')
        options = Options()
        options.page_load_strategy = 'eager'

        if self.headless:
            options.add_argument('--headless')
            options.add_argument("--no-sandbox") 
            options.add_argument("--disable-gpu") 
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--remote-debugging-port=9222")
            options.add_argument('--window-size=1920x1080') # This line is necessary to locate some elements that are hidden when the screen size is small or headless | This is the solution I found to solve this problem
        
        # Supressing SSL warnings
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--allow-running-insecure-content')

        service = Service(CHROME_DRIVER_PATH)
        driver = webdriver.Chrome(service=service, options=options)
        return driver
    
    def get_driver(self):
        return self.driver
    
    def quit_driver(self):
        self.driver.quit()

