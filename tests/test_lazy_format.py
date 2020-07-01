# coding=utf-8
"""
A bunch of tests for the LazyFormat class
"""

import unittest

from lazy_format.format import LazyFormat


class LazyFormatTestCase(unittest.TestCase):
    def test_default(self):
        expectation = 'abcde'
        reality = LazyFormat('abcde')
        self.assertEqual(expectation, reality, 'Default format behavior doesn\'t work')

    def test_default_keyword_param(self):
        expectation = 'abcde'
        reality = LazyFormat('{x}cde').format(x='ab')
        self.assertEqual(expectation, reality, 'Default format behavior doesn\'t work')

    def test_default_ordered_param(self):
        expectation = 'abcde'
        reality = LazyFormat('{0}{x}e').format('ab', x='cd')
        self.assertEqual(expectation, reality, 'Default format behavior doesn\'t work')

    def test_default_extra_format(self):
        expectation = 'ab  cd  e'
        reality = LazyFormat('{0}{x:^6}e').format('ab', x='cd')
        self.assertEqual(expectation, reality, 'Default format behavior doesn\'t work')

    def test_skipping_missed_args(self):
        expectation = '1 {var2} 3 {var4}'
        reality = LazyFormat('{var1} {var2} {var3} {var4}').format(var1=1, var3=3)
        self.assertEqual(expectation, reality, 'Skipping missed variables doesn\'t work')

    def test_format(self):
        expectation = '2 ** 10 = 1024'
        text = '{two} ** {ten} = {result}'

        reality = LazyFormat(text).format(two=2, ten=10, result=2 ** 10)
        self.assertEqual(expectation, reality, 'Format method doesn\'t work properly')

    def test_example(self):
        project = LazyFormat('{name} {0}.{1}.{2} {year} {author}')
        self.assertEqual(project, '{name} {0}.{1}.{2} {year} {author}')

        project = LazyFormat('{name} {0}.{1}.{2} {year} {author}').format(0, 0, 1, year=2013)
        self.assertEqual(project, '{name} 0.0.1 2013 {author}')

        project = LazyFormat('{name} {0}.{1}.{2} {year} {author!s}').format(1, 0, year=2013)
        self.assertEqual(project.format(9, name='lazy format', author='miph'), 'lazy format 1.0.9 2013 miph')
