# coding=utf-8
"""
A bunch of tests for the LazyFormat class
"""

import unittest

from lazy_format.format import LazyFormat


class LazyFormatTestCase(unittest.TestCase):
    def tearDown(self):
        LazyFormat.global_context.clear()

    def test_default(self):
        expectation = 'abcde'
        reality = LazyFormat('abcde')
        self.assertEqual(expectation, reality, 'Default format behavior doesn\'t work')

    def test_default_keyword_param(self):
        expectation = 'abcde'
        reality = LazyFormat('{x}cde', x='ab')
        self.assertEqual(expectation, reality, 'Default format behavior doesn\'t work')

    def test_default_ordered_param(self):
        expectation = 'abcde'
        reality = LazyFormat('{0}{x}e', 'ab', x='cd')
        self.assertEqual(expectation, reality, 'Default format behavior doesn\'t work')

    def test_default_extra_format(self):
        expectation = 'ab  cd  e'
        reality = LazyFormat('{0}{x:^6}e', 'ab', x='cd')
        self.assertEqual(expectation, reality, 'Default format behavior doesn\'t work')

    def test_skipping_missed_args(self):
        expectation = '1 {var2} 3 {var4}'
        reality = LazyFormat('{var1} {var2} {var3} {var4}', var1=1, var3=3)
        self.assertEqual(expectation, reality, 'Skipping missed variables doesn\'t work')

    def test_global_context(self):
        LazyFormat.global_context.clear()
        LazyFormat.global_context.update_context_with({'global_var1': 'GV1', 'global_var2': 'GV2'})

        expectation = 'GV1 GV2'
        reality = LazyFormat('{global_var1} {global_var2}')
        self.assertEqual(expectation, reality, 'Couldn\'t find global context variables')

    def test_global_context_with_intersection(self):
        LazyFormat.global_context.clear()
        LazyFormat.global_context.update_context_with({'global_var1': 'GV1', 'global_var2': 'GV2', 'var1': '123'})

        expectation = 'GV1 GV2 321'
        reality = LazyFormat('{global_var1} {global_var2} {var1}', var1='321')
        self.assertEqual(expectation, reality, 'global parameter var1 wasn\'t overlapped by local')

    def test_format(self):
        expectation = '2 ** 10 = 1024'
        reality = LazyFormat('{two} ** {ten} = {result}')
        reality = reality.format(two=2, ten=10, result=2 ** 10)

        self.assertEqual(expectation, reality, 'Format method doesn\'t work properly')

    def test_example(self):
        project = LazyFormat('{name} {0}.{1}.{2} {year} {author}')
        self.assertEqual(project, '{name} {0}.{1}.{2} {year} {author}')

        project = LazyFormat('{name} {0}.{1}.{2} {year} {author}', 0, 0, 1, year=2013)
        self.assertEqual(project, '{name} 0.0.1 2013 {author}')

        project = LazyFormat('{name} {0}.{1}.{2} {year} {author!s}', 1, 0, year=2013)
        self.assertEqual(project.format(9, name='lazy format', author='miph'), 'lazy format 1.0.9 2013 miph')
