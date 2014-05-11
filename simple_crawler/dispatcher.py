import time
import threading

from .utils import reach_limit


class Worker(object):
    """This class is default worker class for dispatcher, it just print each
    task object.
    """
    def __init__(self, task_obj):
        self.task_obj = task_obj

    def do(self):
        """An interface for dispatcher.
        Implements task handler in this methods.
        """
        print self.task_obj


class Dispatcher(threading.Thread):
    """Dispatcher is a simple wrapper of threading. It gets task from a
    task queue, and then hand out to a worker.
    `worker_class` define which kind of worker you want to hand out tasks.
    If you don't set `worker_class`, dispatcher will just print each
    task object. Here is an example::

        import Queue
        from dispatcher import Dispatcher
        queue = Queue.Queue()
        put_some_task_in(queue)
        dispatcher = Dispatcher(queue)
        dispatcher.start() # start threading

    :param queue: Task queue wait to be handed out.
    """

    worker_class = Worker

    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        """Start threading.
        Each threading get task from task queue and hand out to a worker.
        """
        print 'threading %s start' % self.name
        while True:
            try:
                if reach_limit():
                    print 'Reach limit'
                    break

                if self.queue.empty():
                    print 'queue empty'
                    break

                print "Left: %d" % self.queue.qsize()

                task_obj = self.queue.get()

                worker = self.worker_class(task_obj)
                worker.do()

                self.queue.task_done()

            except Exception as exc:
                print exc
                time.sleep(1)
                continue