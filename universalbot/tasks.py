from background_task import background
from .tasks_signals import task_started, task_finished
from .models import TaskAdaptor

@background
def run_lists(task_id):
	task_started.send(TaskAdaptor, tasks_ids=task_id)
	print(f'> run_lists is fired ({task_id})')

	task_finished.send(TaskAdaptor, tasks_ids=task_id)


