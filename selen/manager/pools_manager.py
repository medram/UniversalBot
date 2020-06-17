from queue import Queue

from selen.common import Singleton
from selen.manager.pool_worker import Pool, Worker
from universalbot.models import Server

@Singleton
class _PoolsManager:

	def __init__(self):
		self._pools = {}
		self._queues = {}


	@staticmethod
	def _get_active_servers():
		return Server.objects.filter(active=True).all()

	def create_pools(self):
		servers = self._get_active_servers()
		for server in servers:
			q = Queue()
			p = Pool(max_workers=server.capacity, queue=q, name=f'Pool_{str(server)}')
			self._pools[server] = p
			self._queues[server] = q
		print(f'create_pools: ({len(self._pools)} pools) ({len(self._queues)} queues)')


	def start_pools(self):
		print('start_pools')
		for pool in self._pools.values():
			pool.start()

	def shutdown_pools(self):
		print('shutdown_pools')
		for pool in self._pools.values():
			pool.shutdown()

	def pause_pools(self):
		print('pause_pools')
		for pool in self._pools.values():
			pool.pause()

	def resume_pools(self):
		print('resume_pools')
		for pool in self._pools.values():
			pool.resume()

	def update_pools(self):
		""" update pools and queues lists """
		servers = self._get_active_servers()

		for server in servers:
			if server not in self._pools:
				# create new pool and its queue for this server.
				q = Queue()
				p = Pool(max_workers=server.capacity, queue=q, name=f'Pool_{str(server)}')
				self._pools[server] = p
				self._queues[server] = q

		for s, p in self._pools.items():
			if s not in servers:
				# delete pool and queue for s
				try:
					del self._pools[s]
					del self._queues[s]
				except KeyError:
					pass

		# TODO: Update pools threads

		print(f'update_pools: ({len(self._pools)} pools) ({len(self._queues)} queues)')
		# print('-' * 60)
		# for p, q in self._queues.items():
		# 	print(f'{p} - {q}, qsize: {q.qsize()}')
		# print('-' * 60)

	def get_pools_needs(self):
		needs = {}
		for s, q in self._queues.items():
			if q.qsize() <= s.capacity * 2:
				needs[s] = s.capacity * 2 - q.qsize()
		print(f'get_pools_needs: {needs}')
		return needs

	def push_subtasks(self, subtasks):
		# subtasks = {
		# 	server1: [(run_profile, (p, l, task)), ()...]
		# }
		print('push_subtasks to pools queues')
		for server, sub_tasks in subtasks.items():
			for subtask in sub_tasks:
				self._queues[server].put(subtask)


PoolsManager = _PoolsManager.get_instance()
