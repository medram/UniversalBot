import time
import threading

"""
TODO: create & start listening on Pools
"""
from selen.manager import PoolsManager
from selen.manager import ATM
from selen.manager.pool_worker import Worker


class RefresherThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(name=None)
        self.name = name
        self._abort = threading.Event()
        self._pools_manager = PoolsManager
        self._atm = ATM

    def abort(self):
        self._abort.set()

    def aborted(self):
        return self._abort.is_set()

    def run(self):
        self._pools_manager.create_pools()
        self._atm.refresh_list()

        while not self.aborted():
            # TODO: refresh pools & lists every 15 secounds
            # TODO: passing new sub_tasks to pools to process
            time.sleep(15)

try:
    t = RefresherThread(name='RefresherThread')

    t.start()
    
    while t.is_alive():
        t.join(0.5)

except (KeyboardInterrupt, SystemExit):
    t.abort()

print('Done.')