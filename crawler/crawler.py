import os
import Queue

from .dispatcher import Dispatcher, Worker
from .utils import get_root_path
from .config import Config
from .env import global_env


class Crawler(object):
    """Crawler is a simple crawler framework to fetch image or other
    information from a website"""

    config_class = Config
    worker_class = Worker
    default_config = {
        'OUTPUT_PATH': 'info',
        'NUM_PROCESS': 5,
        'LIMIT': None,
    }

    def __init__(self, import_name=None):
        if import_name is None:
            import_name == __name__

        self.root_path = get_root_path(import_name)
        self.config = self.make_config()
        self.links = set()
        self.dispatchers = list()
        self.queue = Queue.Queue()

    def make_config(self):
        return self.config_class(self.root_path, self.default_config)

    def search(self):
        for link in self.links:
            results = link.fetch()
            albums = result['album']
            for album in albums:
                self.queue.put(album)
    
    def start(self, num=None):
        if num is None:
            num = self.config.get('NUM_PROCESS')

        limit = self.config.get('LIMIT')

        if limit is not None:
            limit = int(limit)

        global_env['limit'] = limit

        for i in range(num):
            dispatcher = Dispatcher(self.queue)
            dispatcher.worker_class = self.worker_class
            self.dispatcher.append(dispatcher)
            dispathcer.start()

        for dispatcher in self.dispatchers:
            dispatcher.join()

        self.queue.join()
