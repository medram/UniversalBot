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



PoolsManager = _PoolsManager.get_instance()