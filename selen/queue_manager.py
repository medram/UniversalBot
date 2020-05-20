import queue


class MainQueue(queue.Queue):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# a list of taskAdapter queues.
		self.queue_list = []

	def get(self):
		pass
	
	def register(self, q):
		""" register a taskAdapter queue """
		self.queue_list.append(q)

	def unregister(self, q):
		""" unregister a taskAdapter queue """
		del self.queue_list[q]


class QueueManager:

	_instance = None

	def __init__(self):
		# this is the main queue.
		self.main_queue = MainQueue()

	@classmethod
	def get_instance(cls):
		if not cls._instance:
			cls._instance = cls()
		return cls._instance

	def get_main_queue():
		""" Return the main queue """
		self.main_queue

# this is one instance of a QueueManager for the entire application. 
QM = QueueManager.get_instance()