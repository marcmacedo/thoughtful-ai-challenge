from robocorp.tasks import task
# from robocorp.workitems import WorkItem
from RPA.Robocorp.WorkItems import WorkItems

@task
def minimal_task():
    work_item = WorkItems()


    # teste = work_item.get_input_work_item()
    search_phrase = work_item.get_work_item_variable('search_phrase', 'default_value')
    months = work_item.get_work_item_variable('months', 'default_value')
    headless = work_item.get_work_item_variable('headless', 'default_value')

    from src.main import main
    main(search_phrase, months, headless)