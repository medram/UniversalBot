from background_task import background

@background
def run_lists(task_id):
	print(f'> run_lists is fired ({task_id})')