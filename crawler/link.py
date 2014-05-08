#-*- coding: utf-8 -*-
from .utils import fetch_html


class Link(object):
    """Define a link to crawl.
    And items define each part you need to crawl. See :class:`Item`.

    :param name: The name of this link object.
    :param url: The url wait to anaylse.
    :param items: Initialize items set.
    """

    def __init__(self, name, url, items=None):
        self.name = name
        self.url = url
        if items is not None:
            self.items = set(list(items))
        else:
            self.items = set()
        self.html = fetch_html(url)

    def register_funcs(self, funcs):
        """Register clean functions to all items in this object.
        `funcs` is a list of clean functions.

        :param funcs: a list of clean funcs.
        """
        for item in self.items:
            item.clean_funcs = funcs

    def fetch(self):
        """Fetch each item which given by `items` from `url`.
        It call :meth:`fetch` in each item objects, and store result into a
        dictionary. The key of dictionary is name of item, and value is the
        result.
        """
        results = dict()
        for item in self.items:
            result = item.fetch(self.html)
            if result:
                results[item.name] = result
        return results
