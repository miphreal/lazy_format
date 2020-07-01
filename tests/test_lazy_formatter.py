# coding=utf-8
"""
A bunch of tests for the LazyFormatter class
"""

import unittest

from lazy_format.format import LazyFormatter


class LazyFormatterTestCase(unittest.TestCase):
    def setUp(self):
        self.formatter = LazyFormatter()

    def test_default(self):
        expectation = 'abcde'
        reality = str(self.formatter.format('{0}{1}{2}', 'ab', 'cd', 'e'))
        self.assertEqual(expectation, reality, 'Default format behavior doesn\'t work')

    def test_default_keyword_params(self):
        expectation = 'abcde'
        reality = self.formatter.format('{0}{a}{b}', 'ab', a='cd', b='e')
        self.assertEqual(expectation, reality, 'Default format behavior doesn\'t work')

    def test_skipping_missed_args(self):
        expectation = 'abcde{missed_var1}{missed_var2}'
        reality = self.formatter.format('{0}{a}{b}{missed_var1}{missed_var2}', 'ab', a='cd', b='e')
        self.assertEqual(expectation, reality, 'Skipping missed args doesn\'t work')
