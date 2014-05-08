#-*- coding: utf-8 -*-
import os
import unittest

from crawler.config import Config


TEST_KEY = 'key-for-test'
SECRET_KEY = 'secret_key___'


class ConfigTestCase(unittest.TestCase):

    def setUp(self):
        self.root_path = os.path.realpath(os.path.dirname(__file__))
        self.config = Config(self.root_path)

    def test_from_pyfile(self):
        self.config.from_pyfile('config_for_test.py')
        self.assertEqual(self.config['KEY'], 'VALUE')
        self.assertFalse(self.config.from_pyfile('no_file.py', True))
        self.assertRaises(IOError, self.config.from_pyfile, 'no_file.py')

    def test_from_object(self):
        self.config.from_object(__name__)
        self.assertEqual(self.config['TEST_KEY'], 'key-for-test')
        self.assertEqual(self.config['SECRET_KEY'], 'secret_key___')
