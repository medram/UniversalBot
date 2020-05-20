import time
import threading

from .queue_manager import QM


class PoolManager(threading.Thread):
	""" manage thread pool of servers """

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self._stop = threading.Event()
		self._subtask = []


	def run(self):
		while not self.stopped():
			for server in servers:
				with ThreadPoolExecutor(max_workers=server.capacity) as executor:
					# TODO: register an executor
					executor.map(self._run_task, QM.get_main_queue())



			# with ThreadPoolExecutor() as executor:
			# 	futures_list = {executor.submit(run_profile, profile, l, task): profile for l in lists for profile in l.profiles.all()}
			# 	for future in as_completed(futures_list):
			# 		profile = futures_list[future]
			# 		print(f'profile is finished {profile.pk}')
			self._stop.wait(5)
		print(f'{self.getName()} has stopped.')

	@staticmethod
	def _run_task(fn):
		return fn()

	def stop(self):
		self._stop.set()

	def stopped(self):
		return self._stop.is_set()


def main():
	try:
		t = PoolManager(name='pool_manager')
		t.start()
		while t.is_alive():
			t.join(0.5)
	except (KeyboardInterrupt, SystemExit):
		t.stop()


if __name__ == f'{__package__}.process_queue':
	main()