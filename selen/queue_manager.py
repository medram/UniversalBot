import queue
import threading

print(threading.enumerate())
exit()

class MainQueue(queue.Queue):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# a list of taskAdapter queues.
		self.queue_list = []
		self._iter = iter(self.queue_list)
		self._lock = threading.Lock()


	def get(self):
		""" Simulate get queue function """
		
		while True:
			# deny threads from getting access
			self._lock.acquire()
			try:
				q = next(self._iter)
				return q.get(False)
			except StopIteration:
				self._iter = iter(self.queue_list)
				time.sleep(0.5)
			except queue.Empty:
				# raise StopIteration()
				time.sleep(0.5)
			# allow threads to get access
			self._lock.release()


	def register(self, q):
		""" register a taskAdapter queue """
		self.queue_list.append(q)

	def unregister(self, q):
		""" unregister a taskAdapter queue """
		del self.queue_list[q]

	def __next__(self):
		return self.get()

	def __iter__(self):
		return self


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

	def register(self, q):
		""" register a taskAdapter queue """
		self.main_queue.queue_list.append(q)

	def unregister(self, q):
		""" unregister a taskAdapter queue """
		del self.main_queue.queue_list[q]

	def get_main_queue():
		""" Return the main queue """
		self.main_queue

# this is one instance of a QueueManager for the entire application. 
QM = QueueManager.get_instance()