#-*- coding: utf-8 -*-
import re

from .utils import regex_find_named_group


class Item(object):
    """An `Item` defines a regex rule, used to match different part of html.
    `Item` is used by :class:`Link`, and :meth:`fetch` will be called by
    :class:`Link`.

    :param name: The name of this item, it will be a key of dictionary in
                 :class:`Link`.
    :param rule: The regex for this item.
    """
    def __init__(self, name, rule):
        self.clean_funcs = list()
        self.name = name
        self.rule = rule
        self.pattern = re.compile(rule)

    def fetch(self, content):
        """Match pattern in content

        :param content: content wait to find.
        """
        assert(content is not None)
        assert(len(content) > 0)

        results = list()

        rs = regex_find_named_group(self.pattern, content)
        if rs is False:
            return None

        for r in rs:
            r = self.clean_each(r)
            results.append(r)

        self.results = results
        return results

    def clean_each(self, one):
        """Calls each clean functions for each result from :meth:`fetch`.
        """
        for func in self.clean_funcs:
            one = func(one)
        return one
