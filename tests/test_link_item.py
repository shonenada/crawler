#-*- coding: utf-8 -*-
import unittest

from crawler.link import Link
from crawler.item import Item


class LinkItemTestCase(unittest.TestCase):

    def setUp(self):
        self.item = Item('img', r'(?P<img><img [^>]+?>)')
        self.link = Link('movie.douban', 'http://movie.douban.com/', [self.item])

    def test_register_funcs(self):
        def cf(one):
            print one
            return one
        
        self.link.register_funcs([cf])

        self.assertTrue(cf in self.item.clean_funcs)

    def test_fetch(self):
        results = self.link.fetch()
        douban_logo = '<img style="top: -5px; position: relative;" src="http://img3.douban.com/pics/site/icon_site_beta.gif"/>'
        self.assertIn('img', results)

        movie = results['img']
        self.assertIn(douban_logo, [m['img'] for m in movie])
