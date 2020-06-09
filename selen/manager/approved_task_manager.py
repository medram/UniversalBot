import time

from selen import app_settings
from universalbot.models import ATM

from selen.common import Singleton
from universalbot.tasks_signals import task_started, task_finished, each_profile_start, each_profile_end


def run_profile(profile, l, task):
	print('run_profile is processed')
	return None
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



@Singleton
class _ApprovedTaskManager:
	_atm = ATM

	def __init__(self):
		# list of TaskAdapters
		self.tasks = self._load_tasks()
		self._lists = {}
		# self._lists = {
		# 	'taskAdapterID': (
		# 		['server_1', 'server_2'],
		# 		[] # list of profiles
		# 	)
		# }


	def _load_tasks(self):
		"""Return a list of TaskAdapters"""
		return [ atm.task for atm in self._atm.objects.all() ]

	def _refresh_tasks(self):
		self.tasks = self._load_tasks()

	def refresh_list(self):
		self._refresh_tasks()

		# task Not found -> delete it
		ids = [ t.pk for t in self.tasks ] # list of tasks ids
		for task_id in self._lists.keys():
			task_id = int(task_id)
			# not found in new tasks (from db)
			if task_id not in ids:
				del self._lists[str(task_id)]


		# task Not found -> add it
		for task in self.tasks:
			task_id = str(task.pk) # is a string
			if task.pk not in self._lists:
				self._lists[task_id] = (
						[ s for s in task.servers.all() ],
						[ (run_profile, (p, l, task)) for l in task.lists.all() for p in l.profiles.all() ]
					)


	def register(self, task):
		self._atm.objects.create(task=task)

	def unregister(self, task):
		try:
			self._atm.objects.get(task=task).delete()
		except self._atm.DoesNotExist:
			pass

	def get_subtasks(self, s, n):
		# print('>>> LIST:', self._lists)
		# print('=' * 60)
		profile_list = []
		# while len(profile_list) < n:
		for _ in range(n):
			for servers, profiles in self._lists.values():
				# print(servers, profiles)
				if s in servers and len(profile_list) < n and len(profiles):
					profile_list.append(profiles.pop(0))
				# else:
				# 	break

		print('get_subtasks: ', s,len(profile_list))
		return profile_list


ApprovedTaskManager = _ApprovedTaskManager.get_instance()
