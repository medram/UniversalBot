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


def run_profile(profile, l, task):
	""" This funtion execute profile actions using thread pool. """
	each_profile_start.send(profile.__class__, profile=profile, list_=l, task=task)
	try:
		isp = Hotmail(profile, l, task)
		isp.login()
		isp.do_actions()
		isp.quit()
		print(f'profile {profile.pk}...')
		# time.sleep(5)

	except WebDriverException as e:
		if 'Message: Reached error page' in str(e):
			print(f'Please check your internet connection of your server/RDP')
		else:
			print(e)
	except Exception as e:
		print(e)
		# exc_type, exc_value, exc_tb = sys.exc_info()
		# traceback.print_exception(exc_type, exc_value, exc_tb)

	each_profile_end.send(profile.__class__, profile=profile, list_=l, task=task)



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
	



	try:
		task = TaskAdaptor.objects.get(pk=task_id)
	except TaskAdaptor.DoesNotExist:
		pass
	else:
		task.current = 0
		task.progress = 0
		task.save()

		task_started.send(TaskAdaptor, task=task)

		lists = task.lists.all()

		# get active servers.
		# servers = [ s for s in task.servers.all() if s.active ]
		# profiles_list = [ profile for l in lists for profile in l.profiles.all() ]

		for l in lists:
			for profile in l.profiles.all():
				def sub_task():
					return run_profile(profile, l, task)
				# add a sub task to the main queue.
				task._queue.put(sub_task)

				# register a queue to QueueManager
				QM.register(task._queue)

		# for server in servers:
		# 	with ThreadPoolExecutor(max_workers=server.capacity) as executor:
		# 		executor.map(run_profile, profiles_list)



		# with ThreadPoolExecutor() as executor:
		# 	futures_list = {executor.submit(run_profile, profile, l, task): profile for l in lists for profile in l.profiles.all()}
		# 	for future in as_completed(futures_list):
		# 		profile = futures_list[future]
		# 		print(f'profile is finished {profile.pk}')


	print('Done!')

	task_finished.send(TaskAdaptor, task=task)


