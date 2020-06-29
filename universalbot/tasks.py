import time
import sys
import traceback
import queue

from concurrent.futures import ThreadPoolExecutor, as_completed
from .tasks_signals import task_started, task_finished, each_profile_start, each_profile_end
from .models import TaskAdaptor, Deleted_queue

from background_task import background
from selenium.common.exceptions import WebDriverException

from selen.ISP.hotmail import Hotmail
from selen.manager import ApprovedTaskManager


@background
def run_lists(task_id):
	task_id = task_id['task_id']
	# register a task to
	try:
		task = TaskAdaptor.objects.get(pk=task_id)
	except TaskAdaptor.DoesNotExist:
		pass
	else:
		ApprovedTaskManager.register(task)
		print(f'-> The Task ({task_id}) is pushed to Pools.')