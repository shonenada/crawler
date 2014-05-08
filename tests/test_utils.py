#-*- coding: utf-8 -*-
import os
import re
import unittest

from crawler import utils


class UtilsTestCase(unittest.TestCase):

    def setUp(self):
        self.root_path = os.path.dirname(os.path.abspath(__file__))

    def test_import_string(self):
        import_string = utils.import_string
        import cgi
        self.assertEqual(import_string('cgi.escape'), cgi.escape)
        self.assertEqual(import_string(u'cgi.escape'), cgi.escape)
        self.assertIsNone(import_string('nothing.nothing', True))
        self.assertIsNone(import_string('cgi.nothing', True))
        self.assertRaises(ImportError, import_string, 'nothing.nothing')
        self.assertRaises(ImportError, import_string, 'cgi.nothing')

    def test_get_root_path(self):
        get_root_path = utils.get_root_path
        self.assertTrue(get_root_path('crawler.utils'), __file__)
        self.assertTrue(get_root_path('no_exist'), os.getcwd())
        self.assertTrue(get_root_path('tests.for_test'), self.root_path)

    def test_regex_find_named_group(self):
        regex_find_named_group = utils.regex_find_named_group
        names = 'bob sue john harry'
        pattern = re.compile(r'(?P<name>\w+)')
        self.assertEqual(regex_find_named_group(pattern, names),
                         [{'name': 'bob'}, {'name': 'sue'},
                          {'name': 'john'}, {'name': 'harry'}])
        name = 'Harry Potter'
        name_pattern = re.compile(r'(?P<firstname>\w+) (?P<lastname>\w+)')
        self.assertEqual(regex_find_named_group(name_pattern, name),
                         [{'firstname': 'Harry', 'lastname': 'Potter'}])

        sth = 'asdfghjl'
        digital_pattern = re.compile(r'\d+')
        self.assertFalse(regex_find_named_group(digital_pattern, sth))

    def test_fetch_html(self):
        fetch_html = utils.fetch_html
        no_exist_url = 'http://www.douban.com/nononono'
        self.assertTrue(fetch_html(no_exist_url) == None)
