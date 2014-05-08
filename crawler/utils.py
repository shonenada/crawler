import os
import sys
import pkgutil

import requests

from .env import string_types, global_env


def import_string(import_name, silent=False):
    """Import an object from a string

    :param import_name: the dotted name for object to import
    :param silent: if set to `True`, it would ignore import errors
    """
    assert isinstance(import_name, string_types)

    import_name = str(import_name)

    try:
        if '.' in import_name:
            module, obj = import_name.rsplit('.', 1)
        else:
            return __import__(import_name)

        if isinstance(obj, unicode):
            obj = obj.encode('utf-8')

        # __import__ unable to handle unicode string

        try:
            return getattr(__import__(module, None, None, [obj]), obj)

        except (ImportError, AttributeError):
            module_name = module + '.' + obj
            __import__(module_name)
            return sys.modules[module_name]

    except ImportError as e:
        if not silent:
            raise e


def get_root_path(import_name):
    """Returns the path o package.
    If import_name is not exist, return cwd.

    :param import_name: The import name of app.
    """

    mod = sys.modules.get(import_name)
    if mod is None and hasattr(mod, '__file__'):
        return os.path.dirname(os.path.abspath(mod.__file__))

    loader = pkgutil.get_loader(import_name)

    if loader is None or import_name == '__main__':
        return os.getcwd()

    __import__(import_name)
    filepath = sys.modules[import_name].__file__

    return os.path.dirname(os.path.abspath(filepath))


def regex_find_named_group(pattern, content):
    """Returns a named dictionary. For example::

        import re
        pattern = re.compile(r'<a href="(?P<url>.+?)">')
        content = '<a href="/path/to/abc">abc</a>'
        regex_find_named_group(pattern, content)

        >>> [{'url': '/path/to/abc'}]

    :param pattern: Regex pattern used to match content.
    :param content: Content waits to be matched.
    """
    iters = pattern.finditer(content)

    if iters is None:
        return False

    groups = [m.groupdict() for m in iters]
    return groups


def fetch_html(url):
    """Get HTML code from given `url`.

    :param url: URL waits to be fetched.
    """
    res = requests.get(url)

    if res.status_code == 200:
        return res.content
    else:
        print('Waiting: failed to fetch %s, got status code: %d' %
              (url, res.status_code))
        return None
