from robocorp.tasks import task, get_work_item
from src.main import main
import subprocess

@task
def minimal_task():
    work_item = get_work_item()

    search_phrase = work_item.get('search_phrase', 'Sports')
    months = work_item.get('months', 0)
    headless = work_item.get('headless', True)

    subprocess.run(['python', 'src/main.py', (search_phrase, months, headless)])