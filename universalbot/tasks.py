import time
import sys
import traceback


from concurrent.futures import ThreadPoolExecutor, as_completed
from .tasks_signals import task_started, task_finished, each_profile_start, each_profile_end
from .models import TaskAdaptor

from background_task import background
from selenium.common.exceptions import WebDriverException

from selen.ISP.hotmail import Hotmail


def run_profile(profile, l, task):
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
	print('> Task:', task_id)
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

		with ThreadPoolExecutor() as executor:	
			futures_list = {executor.submit(run_profile, profile, l, task): profile for l in lists for profile in l.profiles.all()}
			for future in as_completed(futures_list):
				profile = futures_list[future]
				print(f'profile is finished {profile.pk}')


	print('Done!')

	task_finished.send(TaskAdaptor, task=task)


