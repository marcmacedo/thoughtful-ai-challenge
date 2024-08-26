from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from datetime import datetime, timedelta
from dateutil import parser
from config import IMAGES_PATH
import re, requests, hashlib, os


class NewsScraper:
    def __init__(self, driver, search_phrase, category=None, months=0):
        self.driver = driver
        self.search_phrase = search_phrase
        self.category = category
        self.months = months

    def search_news(self, url):
        self.driver.get(url)


        WebDriverWait(self.driver, 30).until(
            lambda driver: driver.execute_script('return document.readyState') == 'complete'
        ) # Waiting for page to fully load before scraping


        # Clicking on search icon
        search_icon = self.driver.find_element(By.CSS_SELECTOR, "svg[class*='icon icon--search icon--grey icon--24 ']")
        search_icon.click()


        # Finding search bar and searching text
        search_box = self.driver.find_element(By.XPATH, "//*[@id=\"root\"]/div/div[1]/div[2]/div/div/form/div[1]/input")
        search_box.click()
        search_box.send_keys(self.search_phrase)
        search_box.submit()


        WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//*[@id="main-content-area"]/div[2]/div[1]/div/div'))
        )


        filter_by_date = self.driver.find_element(By.XPATH, '//*[@id="search-sort-option"]')
        filter_by_date = Select(filter_by_date)
        filter_by_date.select_by_value('date')


        try:
            while True:
                show_more_button = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '#main-content-area > div.l-col.l-col--8 > div.search-result__list > button'))
                )
                self.driver.execute_script("arguments[0].click();", show_more_button)


        except:
            print(f"'Show more' button not found, terminating loop.")



    # --------------------------------
    def scrape_result(self):
        current_date = datetime.now()
        start_date = current_date - timedelta(days=30 * (self.months + 1 if self.months > 0 else 1))


        news_data = []
        i = 1

        # Waiting results
        news_elements = WebDriverWait(self.driver, 15).until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "gc__content")]'))
        )


        # Scrapping results
        for news in news_elements:
            try:
                    
                title = news.find_element(By.XPATH, './/h3').text
                url = news.find_element(By.XPATH, './/h3/a').get_attribute('href')

                try:
                    description = news.find_element(By.XPATH, f"//*[@id=\"main-content-area\"]/div[2]/div[2]/article[{i}]/div[2]/div[2]/div").text
                    
                    match = re.match(r'(?P<creation_date>.+?)\s+\.\.\.\s+(?P<description>.+)', description)

                    # Creation date is inside description text
                    creation_date_str = match.group('creation_date')
                    description = match.group('description')

                    try:
                        creation_date = parser.parse(creation_date_str)
                    except ValueError:
                        if "hour" in creation_date_str or "minute" in creation_date_str or "day" in creation_date_str:
                            creation_date = current_date - timedelta(hours=int(re.search(r'\d+', creation_date_str).group()))
                        else:
                            creation_date = None
                    

                except:
                    description = "No description found"

                try:
                    last_update = news.find_element(By.XPATH, f"//*[@id=\"main-content-area\"]/div[2]/div[2]/article[{i}]/div[2]/footer/div/div/div/div/span[1]").text
                except:
                    last_update = "No info found"

                
                
                if creation_date and creation_date >= start_date:
                    img_elements = news.find_elements(By.XPATH, f'//*[@id="main-content-area"]/div[2]/div[2]/article[{i}]/div[3]/div/div/img')
                    img_url = img_elements[0].get_attribute('src') if img_elements else None

                    if img_url:
                        img_name = hashlib.md5(img_url.encode()).hexdigest() + '.jpg'
                        img_path = os.path.join(IMAGES_PATH, img_name)

                        img_data = requests.get(img_url).content
                        with open(img_path, 'wb') as img_file:
                            img_file.write(img_data)
                    
                    else:
                        img_name = "No image found"
                    
                    has_money = bool(re.search(r"\$\d+(\.\d{2})?|\d+ dollars|\d+ USD", title + description))
                    
                    
                    news_data.append({
                        "title": title,
                        "creation_date": creation_date_str,
                        "last_update": last_update,
                        "description": description,
                        "img_name": img_name,
                        "has_money": has_money,
                        "url": url
                    })

            except Exception as e:
                print(f"Error extracting data: {e}")
            i += 1
        return news_data
