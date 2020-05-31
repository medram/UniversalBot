import time
import threading

"""
TODO: create & start listening on Pools
"""
from selen.manager import PoolsManager
from selen.manager import ATM
from selen.manager.pool_worker import Worker


class RefresherThread(threading.Thread):
    def __init__(self, name=None):
        threading.Thread.__init__()
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
            self._pools_manager.update_pools()
            self._atm.refresh_list()
            # TODO: passing new sub_tasks to pools to process
            self.passing_subtasks_to_pools()
            time.sleep(15)


    def passing_subtasks_to_pools(self):
        # get the necessary sub_tasks number from queues
        needs = self._pools_manager.get_pools_needs()
        # get these sub_tasks
        subtasks = self.get_subtasks(needs)
        # appending these sub_tasks to pools queues
        self._pools_manager.push_subtasks(subtasks)


    def get_subtasks(self, needs):
        subtasks = {}
        for s, n in needs.items():
            subtasks[s] = self._atm.get_subtasks(s, n)
            
        return subtasks




def main():
    try:
        t = RefresherThread(name='RefresherThread')

        t.start()
        
        while t.is_alive():
            t.join(0.5)

    except (KeyboardInterrupt, SystemExit):
        t.abort()

    print('Done.')


if __name__ == '__main__':
    main()
