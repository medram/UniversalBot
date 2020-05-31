from selen import app_settings
from universalbot.models import ATM


class ApprovedTaskManager:
	_atm = ATM
	
	def __init__(self):
		self.tasks = self._load_tasks()
		self._lists = {}
		# self._lists = {
		# 	'taskID': (
		# 		['server_1', 'server_2'],
		# 		[] # list of profiles
		# 	)
		# }


	def _load_tasks(self):
		return _atm.objects.all()

	def _refresh_tasks(self):
		self.tasks = self._load_tasks()

	def _refresh_lists(self):
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
						[ p for l in task.lists.all() for p in l.profiles.all() ]
					)


	@staticmethod
	def register(task):
		_atm.objects.create(task=task)

	@staticmethod
	def unregister(task):
		task.delete()