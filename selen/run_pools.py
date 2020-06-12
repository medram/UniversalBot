import time
import threading

"""
TODO: create & start listening on Pools
"""
from selen.manager import PoolsManager
from selen.manager import ApprovedTaskManager
from selen.manager.pool_worker import Worker


class ThreadRefresher(threading.Thread):
    def __init__(self, name=None):
        threading.Thread.__init__(self)
        self.name = name
        self._abort = threading.Event()
        self._pools_manager = PoolsManager
        self._approved_task_manager = ApprovedTaskManager

    def abort(self):
        self._abort.set()
        print('abort ThreadRefresher')
        self._pools_manager.shutdown_pools()

    def aborted(self):
        return self._abort.is_set()

    def run(self):
        self._pools_manager.create_pools()
        self._pools_manager.start_pools()
        # self._approved_task_manager.refresh_list()

        while not self.aborted():
            # refresh pools & lists every x secounds
            self._pools_manager.update_pools()
            self._approved_task_manager.refresh_list()
            # passing new sub_tasks to pools to process
            self.passing_subtasks_to_pools()
            print('waiting 5s...')
            self._abort.wait(5)


    def passing_subtasks_to_pools(self):
        print('passing_subtasks_to_pools')
        # get the necessary sub_tasks number from queues
        needs = self._pools_manager.get_pools_needs()
        # get these sub_tasks
        subtasks = self.get_subtasks(needs)
        # appending these sub_tasks to pools queues
        self._pools_manager.push_subtasks(subtasks)


    def get_subtasks(self, needs):
        subtasks = {}
        for s, n in needs.items():
            subtasks[s] = self._approved_task_manager.get_subtasks(s, n)
        # print(f'get_subtasks: {subtasks} -> {s}')
        return subtasks




def main():
    try:
        t = ThreadRefresher(name='ThreadRefresher')

        t.start()

        while t.is_alive():
            t.join(0.5)

    except (KeyboardInterrupt, SystemExit):
        t.abort()

    print('Done.')

if __name__ == f'{__package__}.run_pools':
    main()
