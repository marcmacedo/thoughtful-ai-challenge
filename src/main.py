from config import DEFAULT_SEARCH_URL, MAX_RETRIES, OUTPUT_FILES_PATH
from web_driver_manager import WebDrvierManager
from news_scraper import NewsScraper
from excel_exporter import ExcelExporter
from selenium.common.exceptions import TimeoutException
from datetime import datetime
from logger import setup_logger
import warnings
warnings.filterwarnings("ignore")

logger = setup_logger()


def main():
    driver_manager = WebDrvierManager(headless=True)
    driver = driver_manager.get_driver()

    retry_attempts = 0 
    while retry_attempts < MAX_RETRIES:
        try:
            scraper = NewsScraper(driver, search_phrase="São Paulo", months=0)
            scraper.search_news(DEFAULT_SEARCH_URL)
            news_data = scraper.scrape_result()
            logger.info('Data collected, validating payload...')


            if isinstance(news_data, list):
                logger.info('Payload validated, exporting to sheet format')
                file_name = (datetime.now()).strftime('%m_%d_%Y-%Hh%mmin')
                file_name = f'{str(file_name)}_news_data.xlsx'
                exporter = ExcelExporter(news_data, output_path=f'{OUTPUT_FILES_PATH}{file_name}')
                exporter.export_to_excel()
                logger.info(f'File exported to "{OUTPUT_FILES_PATH}" with name {file_name}')
                break

        except TimeoutException:
            retry_attempts += 1
            logger.warning(f'Got any response, retrying. Max tries={MAX_RETRIES}, current try={retry_attempts} ')

    


    driver_manager.quit_driver()

if __name__ == '__main__':

    main()