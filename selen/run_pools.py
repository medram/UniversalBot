import os
import time
import threading
import random

from queue import Queue


def execption_handler(thread_name, exception):
    print(f'{thread_name}: {exception}')


class Worker(threading.Thread):

    def __init__(self, name, queue, result, wait_queue=False, callback=None, 
        execption_handler=execption_handler):

        threading.Thread.__init__(self)
        self.name = name
        self.queue = queue
        self.result = result
        self._abort = threading.Event()
        self._idle = threading.Event()
        self._pause = threading.Event()
        self.callback = callback
        self.execption_handler = execption_handler
        self.wait_queue = wait_queue


    def abort(self, block=True):
        self._abort.set()
        # print(f'{self.name} is stopping...')
        while block and self.is_alive():
            time.sleep(0.5)
        print(f'{self.name} is stopped')

    def aborted(self):
        return self._abort.is_set()
    
    def pause(self):
        self._pause.set()
        self._idle.set()

    def resume(self):
        self._pause.clear()
        self._idle.clear()

    def paused(self):
        return self._pause.is_set()

    def __del__(self):
        if not self.aborted():
            self.abort()
        # print(f'{self.name} is deleted')

    def _pause_now(self):
        """ block the code for a while """
        while self.paused():
            print(f'{self.name} paused for 0.5s...')
            time.sleep(0.5)

    def block(self, block=True):
        while block and self.is_alive():
            time.sleep(0.5)

    def run(self):
        while not self.aborted():
            try:
                func, args, kwargs = self.queue.get(timeout=0.5)
                # func = self.queue.get(timeout=0.5)
                self._idle.clear()
            except Exception:
                # the queue is empty.
                print(f'{self.name}: The Queue is empty.')
                self._idle.set()
                # abort the thread if the queue is empty.
                if not self.wait_queue:
                    break
                continue

            # the task is available to work with.
            try:
                print(f'{self.name} processing...')
                r = func(*args, **kwargs)
                self.result.put(r)
                if self.callback:
                    self.callback(r)
                
            except Exception as e:
                print('Exception has occured')
                self.execption_handler(self.name, e)
            finally:
                self.queue.task_done()
                # self._abort.wait(1)

            # pause the thread is _pause flag is set
            self._pause_now()


class Pool:
    def __init__(self, max_workers=os.cpu_count() + 4, name=None, queue=None, wait_queue=True, 
        result_queue=None, callback=None, execption_handler=execption_handler):
        self.name = name
        self.max_worker = max_workers
        self.callback = callback
        self.execption_handler = execption_handler
        
        self.queue = queue if isinstance(queue, Queue) else Queue()
        self.result_queue = result_queue if isinstance(result_queue, Queue) else Queue()
        self.wait_queue = wait_queue

        # self.idles = []
        # self.aborts = []
        self.threads = []


    def start(self):
        # reinitialize values
        # self.idles = []
        # self.aborts = []
        self.threads = []
        self.result_queue = result_queue if isinstance(result_queue, Queue) else Queue()

        # create all threads
        for i in range(self.max_worker):
            self.threads.append(Worker(f'Worker_{i} ({self.name})', self.queue, self.result_queue, wait_queue=self.wait_queue, callback=self.callback))

        # start all threads
        for t in self.threads:
            t.start()

        print(self.threads)
        return True

    def is_alive(self):
        return any((t.is_alive() for t in self.threads))

    def is_idle(self):
        return False not in (t.idle() for t in self.threads)

    def is_done(self):
        return self.queue.empty()

    def shutdown(self, block=False):
        """ Abort all threads in the pool """
        for t in self.threads:
            t.resume() # the thread should be working to abort it.
            t.abort()
        self.block(block)
        print(f'{self.name} is shutted down')

    def join(self, timeout=None):
        """ wait until all the queue tasks be completed """
        if timeout and self.is_alive():
            time.sleep(timeout)
        else:
            self.queue.join()

    def result(self, block=False):
        """ return result as generator """
        result = []
        if block and self.is_alive():
            self.join()
        try:
            while True:
                result.append(self.result_queue.get(False))
                self.result_queue.task_done()
        except:
            # the result_queue is emply
            pass

        return result

    def __del__(self):
        self.shutdown()
        print(f'{self.name} is deleted')

    def is_paused(self):
        return False not in ( t.paused() for t in self.threads )

    def pause(self, timeout=0, block=False):
        """ after_abort: pause an amount of time (timeout) after all threads of the pool has stopped/aborted """
        print(f'>>>>>>>>>> {self.name} is paused <<<<<<<<<<<<')
        for t in self.threads:
            t.pause()
        if timeout:
            # if block:
            #     # to make sure start counting after all threads are paused. 
            #     while self.is_paused():
            #         print(f'{self.name} sleeping 0.2s...({self.is_paused()})')
            #         time.sleep(0.2)
            # print('>>>> Loop is finished')
            time.sleep(timeout)
            self.resume()
        return True

    def resume(self, block=False):
        print(f'>>>>>>>>>> {self.name} is resumed <<<<<<<<<<<<')
        for t in self.threads:
            t.resume()
        return True

    def block(self, block=True):
        while block and self.is_alive():
            time.sleep(0.5)


task_queue = Queue()
result_queue = Queue()

def process(i, name='test'):
    time.sleep(0.5)
    return i * i

for i in range(10):
    task_queue.put((process, (i,), {'name':'test'}))


def add_to_queue(q):
    for i in range(20):
        print(f'Adding ({i}) to the queue')
        q.put((process, (i,), {'name':'test'}))
        time.sleep(random.uniform(0, 1))


try:
    t = threading.Thread(target=add_to_queue, args=(task_queue,))
    p = Pool(max_workers=4, name='MyPool', queue=task_queue, result_queue=result_queue)
    # return the control to the main thread.
    t.start()
    p.start()

    time.sleep(5)
    p.pause(timeout=5)
    # p.pause()
    # time.sleep(5)
    # p.resume()

    while p.is_alive():
        p.join(0.5)
    
    # while t.is_alive():
    #     t.join(0.5)

except KeyboardInterrupt:
    p.shutdown()

print('Done.')

print('####### Result #######')
for i in range(p.result_queue.qsize()):
    print(p.result_queue.get())
# print(p.result())
# time.sleep(5)
# print(f'Size: {result_queue.qsize()}')





















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
