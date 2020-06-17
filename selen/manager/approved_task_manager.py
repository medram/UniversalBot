import time
import threading

from selen import app_settings
from universalbot.models import ATM, TaskAdaptor

from selen.common import Singleton
from universalbot.tasks_signals import ( task_started, task_finished, each_profile_start, 
		each_profile_end, on_approved_task_manager_refresh_list)


def run_profile(profile, l, task):
	time.sleep(2)
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


def sync_list(f):
	""" Sync access to the self._lists variable """
	def decorated(*args, **kwargs):
		# wait until acquiring the list lock.
		while ApprovedTaskManager._list_lock.is_set():
			time.sleep(0.5)

		# acquire the lock
		ApprovedTaskManager._list_lock.set()
		result = f(*args, **kwargs)
		# release the lock
		ApprovedTaskManager._list_lock.clear()
		return result

	return decorated


@Singleton
class _ApprovedTaskManager:
	_atm = ATM
	_list_lock = threading.Event()

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

	@sync_list
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
			if task_id not in self._lists:
				self._lists[task_id] = (
						[ s for s in task.servers.all() ],
						[ (run_profile, (p, l, task), {}) for l in task.lists.all() for p in l.profiles.filter(status=True).all() ]
					)
				
				# try to update task_adapter if exists
				try:
					task_adaptor = self._get_taskAdaptor(task_id)
					task_adaptor.total_qsize = len(self._lists[task_id][1])
					task_adaptor.save()

					self.report_taskAdapter_as_not_completed(task_adaptor)
				except Exception:
					pass

		print(f'refresh_list: ({len(self._lists)} subtasks lists in list)')

		task_ids_to_delete = []
		# delete the list  if the task list is empty. 
		for task_id, value in self._lists.items():
			if len(value[1]) == 0:
				print(f'===> deleting {task_id}')
				task_ids_to_delete.append(task_id)

		#fire a signal
		on_approved_task_manager_refresh_list.send(ApprovedTaskManager.__class__, lists=self._lists)

		# delete the list from self._lists
		for task_id in task_ids_to_delete:
			del self._lists[task_id] # task_id is a string

			# unregister a TaskAdaptor from a database if its list of sub_tasks is empty.
			taskAdaptor = self._get_taskAdaptor(task_id)
			if taskAdaptor:
				self.unregister(taskAdaptor)
				self.report_taskAdapter_as_completed(taskAdaptor)




	@staticmethod
	def _get_taskAdaptor(task_id):
		task_id = int(task_id)
		try:
			return TaskAdaptor.objects.get(pk=task_id)
		except TaskAdaptor.DoesNotExist:
			return None

	def register(self, task):
		try:
			task.completed_task = False
			task.save()
		except:
			pass
		self._atm.objects.create(task=task)

	def unregister(self, task):
		try:
			self._atm.objects.get(task=task).delete()
		except self._atm.DoesNotExist:
			pass

	@sync_list
	def get_subtasks(self, s, n):
		# print('=' * 60)
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

		print('ATM get_subtasks: ', s, len(profile_list), 'subtasks')
		# print('lists:', self._lists)
		return profile_list


	@staticmethod
	def report_taskAdapter_as_completed(task_adapter):
		# task is a task adapter
		try:
			task_adapter.queue_status = task_adapter.QUEUE_STATUS.COMPLETED
			task_adapter.save()
		except Exception:
			pass

	@staticmethod
	def report_taskAdapter_as_not_completed(task_adapter):
		# task is a task adapter
		try:
			task_adapter.queue_status = task_adapter.QUEUE_STATUS.PROCESSING
			task_adapter.save()
		except Exception:
			pass


ApprovedTaskManager = _ApprovedTaskManager.get_instance()
