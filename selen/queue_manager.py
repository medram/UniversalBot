import queue
import threading

from selen.common import Singleton

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


@Singleton
class QueueManager:

	def __init__(self):
		# this is the main queue.
		self.main_queue = MainQueue()

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

# class MainQueue(queue.Queue):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # a list of taskAdapter queues.
#         self.queue_list = []
#         self._iter = iter(self.queue_list)
#         self._lock = threading.Lock()


#     def get(self):
#         """ Simulate get queue function """
#         print('get a next value')
#         while True:
#             print('lock')
#             # deny threads from getting access
#             self._lock.acquire()
#             try:
#                 q = next(self._iter)
#                 value = q.get(False)
#                 break
#             except StopIteration:
#                 print('StopIteration')
#                 self._iter = iter(self.queue_list)
#                 # time.sleep(0.5)
#             except queue.Empty:

#                 # print('queue.Empty')
#                 print('remove', q)
#                 self.queue_list.remove(q)
#                 # del self.queue_list[q]
#                 time.sleep(0.5)
#             # allow threads to get access
#             self._lock.release()
#             print('unlock')

#         # allow threads to get access
#         self._lock.release()
#         print('unlock')
        
#         print('return', value)
#         return value


#     def register(self, q):
#         """ register a taskAdapter queue """
#         self.queue_list.append(q)

#     def unregister(self, q):
#         """ unregister a taskAdapter queue """
#         self.queue_list.remove(q)

#     def __next__(self):
#         return self.get()

#     def __iter__(self):
#         return self

# mq = MainQueue()

# q1 = queue.Queue()
# q2 = queue.Queue()
# q3 = queue.Queue()

# for i in range(10):
#     q1.put(f'Q1_{i}')

# for i in range(5):
#     q2.put(f'Q2_{i}')

# for i in range(15):
#     q3.put(f'Q3_{i}')

# mq.register(q1)
# mq.register(q2)
# mq.register(q3)

# def process(n):
#     time.sleep(1)
#     print('processing...', n)
#     return True

# with ThreadPoolExecutor(max_workers=4) as executor:
#     futures = executor.map(process, mq)

# print(futures)
