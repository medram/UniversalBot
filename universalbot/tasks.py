import time
import sys
import traceback
import queue

from concurrent.futures import ThreadPoolExecutor, as_completed
from .tasks_signals import task_started, task_finished, each_profile_start, each_profile_end
from .models import TaskAdaptor

from background_task import background
from selenium.common.exceptions import WebDriverException

from selen.ISP.hotmail import Hotmail
from selen.queue_manager import QM
from selen.manager import ApprovedTaskManager

# main queue.
# sub_tasks_queue = queue.Queue()


@background
def run_lists(task_id):
	task_id = task_id['task_id']
	# register a task to
	try:
		task = TaskAdaptor.objects.get(pk=task_id)
	except TaskAdaptor.DoesNotExist:
		pass
	else:
		ApprovedTaskManager.register(task_id)
		print(f'-> The Task ({task_id}) is pushed to Pools.')
	
	# try:
	# 	task = TaskAdaptor.objects.get(pk=task_id)
	# except TaskAdaptor.DoesNotExist:
	# 	pass
	# else:
	# 	task.current = 0
	# 	task.progress = 0
	# 	task.save()

	# 	task_started.send(TaskAdaptor, task=task)

	# 	lists = task.lists.all()

	# 	for l in lists:
	# 		for profile in l.profiles.all():
	# 			def sub_task():
	# 				return run_profile(profile, l, task)
	# 			# add a sub task to the main queue.
	# 			task._queue.put(sub_task)

	# 			# register a queue to QueueManager
	# 			QM.register(task._queue)

	print('Done!')

	task_finished.send(TaskAdaptor, task=task)


