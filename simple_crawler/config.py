import os
import imp
import errno

from .utils import import_string
from .env import string_types


class Config(dict):
    """An extensional dictionary with method to load config from files.

    :param root_path: The root path of app.
    """

    def __init__(self, root_path, default=None):
        dict.__init__(self, default or {})
        self.root_path = root_path

    def from_pyfile(self, filename, silent=False):
        """Load config from a Python file.

        :param filename: The filename of config.
        :param silent: set to `True` if you want silent warnings.
        """
        filename = os.path.join(self.root_path, filename)
        mdl = imp.new_module('config')
        mdl.__file__ = filename

        try:
            with open(filename) as config_file:
                exec(compile(config_file.read(), filename, 'exec'),
                     mdl.__dict__)
        except IOError as e:
            if silent and e.errno in (errno.ENOENT, errno.EISDIR):
                return False
            e.strerror = 'Unable to load file: %s' % e.strerror
            raise e
        self.from_object(mdl)
        return True

    def from_object(self, obj):
        """Load configs from give object. An object should be one of:
        - a string: the name of object will be imported.
        - an object reference.
        
        :param obj: an import name of object
        """
        if isinstance(obj, string_types):
            obj = import_string(obj)
        for key in dir(obj):
            if key.isupper():
                self[key] = getattr(obj, key)
