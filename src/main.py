from config import DEFAULT_SEARCH_URL, MAX_RETRIES, OUTPUT_FILES_PATH
from web_driver_manager import WebDrvierManager
from news_scraper import NewsScraper
from excel_exporter import ExcelExporter
from selenium.common.exceptions import TimeoutException
from datetime import datetime
from logger import setup_logger

logger = setup_logger()

def validate_input(search_phrase, months):
    if not isinstance(search_phrase, str):
        raise TypeError("Parameter 'search_phrase' must be str type.")
    if not search_phrase.strip():
        raise ValueError("Parameter 'search_phrase' cannot be blank or null.")

    if not isinstance(months, int):
        raise TypeError("Parameter 'months' must bem int type.")
    if months < 0:
        raise ValueError("Parameter 'months' must be positive.")


def main(search_phrase, months):
    try:
        validate_input(search_phrase, months)
        driver_manager = WebDrvierManager(headless=True)
        driver = driver_manager.get_driver()

        retry_attempts = 0 
        while retry_attempts < MAX_RETRIES:
            try:
                scraper = NewsScraper(driver, search_phrase=str(search_phrase), months=int(months))
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

    except:
        logger.error(f'Wrong parameters type or values')



if __name__ == '__main__':
    main(search_phrase, months)