import os
import json

CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'config', 'config.json')


def load_config():
    with open(CONFIG_PATH, 'r') as config_file:
        config = json.load(config_file)
    return config


def create_directories():
    os.makedirs(LOG_FILE_PATH, exist_ok=True)
    os.makedirs(IMAGES_PATH, exist_ok=True)
    os.makedirs(OUTPUT_FILES_PATH, exist_ok=True)

    for filename in os.listdir(IMAGES_PATH):
        file_path = os.path.join(IMAGES_PATH, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Fail to delete files in {IMAGES_PATH}: {e}")


config = load_config()

LOG_FILE_PATH = config.get('log_file_path')
IMAGES_PATH = config.get('images_path')
OUTPUT_FILES_PATH = config.get('output_files_path')
CHROME_DRIVER_PATH = config.get('chrome_driver_path')
DEFAULT_SEARCH_URL = config.get('default_search_url')
MAX_RETRIES = config.get('max_retries')

create_directories()