import time

from .tasks_signals import task_started, task_finished, each_profile_start, each_profile_end
from .models import TaskAdaptor

from background_task import background
from selenium.common.exceptions import WebDriverException

from selen.ISP.hotmail import Hotmail


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

		for l in lists:
			for profile in l.profiles.all():
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
				each_profile_end.send(profile.__class__, profile=profile, list_=l, task=task)

	print('Done!')

	task_finished.send(TaskAdaptor, task=task)


