from robocorp.tasks import task
from RPA.Robocorp.WorkItems import WorkItems
from src.main import main

@task
def minimal_task():
    wi = WorkItems()
    wi.get_input_work_item()

    search_phrase = wi.get_work_item_variable('search_phrase')
    months = wi.get_work_item_variable('months')

    main(search_phrase, months)