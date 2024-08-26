from config import DEFAULT_SEARCH_URL
from web_driver_manager import WebDrvierManager
from news_scraper import NewsScraper
from news_filter import NewsFilter
from excel_exporter import ExcelExporter
from selenium.common.exceptions import TimeoutException

import json

def main():
    driver_manager = WebDrvierManager(headless=False)
    driver = driver_manager.get_driver()

    retry_attempts = 0 
    while retry_attempts < 3:
        try:
            scraper = NewsScraper(driver, search_phrase="Sports", months=3)
            scraper.search_news(DEFAULT_SEARCH_URL)
            news_data = scraper.scrape_result()
            print(json.dumps(news_data, indent=4, ensure_ascii=False))
            print(len(news_data))

            if isinstance(news_data, list) and len(news_data) > 0:
                break

        except TimeoutException:
            print(f"Timeout error. Retrying.")
            retry_attempts += 1
    # filter = NewsFilter(news_data, months=2)
    # filtered_news = filter.filter_by_date()

    # exporter = ExcelExporter(filtered_news, output_path='output/news_data.xlsx')
    # exporter.export_to_excel()

    driver_manager.quit_driver()

if __name__ == '__main__':
    main()