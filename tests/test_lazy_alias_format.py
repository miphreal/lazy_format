# coding=utf-8
"""
A bunch of tests for the LazyAliasFormat class
"""

import unittest

from lazy_format.aliases import Aliases
from lazy_format.format import LazyAliasFormat


class LazyAliasFormatTestCase(unittest.TestCase):
    def tearDown(self):
        Aliases.clear_aliases()

    def test_simple_alias(self):
        Aliases.add_alias('project_name', 'LazyFormat')

        lazy = LazyAliasFormat('{alias.project_name}')
        self.assertEqual(lazy, 'LazyFormat')

    def test_simple_alias_with_intersection(self):
        Aliases.add_alias('project_name', 'LazyFormat')

        lazy = LazyAliasFormat('{project_name} {alias.project_name}', project_name='prj')
        self.assertEqual(lazy, 'prj LazyFormat')

    def test_alias_value_as_function(self):
        def func(alias, context):
            return 'dyn value for ' + alias

        Aliases.add_alias('val', func)

        lazy = LazyAliasFormat('{alias.val}')
        self.assertEqual(lazy, 'dyn value for val')

    def test_default_use_case(self):
        LazyAliasFormat('{project_dir}', alias='dir')

        templates = LazyAliasFormat('{alias.dir}/{template_dir_name}',
                                    template_dir_name='templates',
                                    alias='template_dir')

        my_prj_templates = LazyAliasFormat('{alias.template_dir}',
                                           project_dir='/code/lazy_format',
                                           template_dir_name='tmps')

        self.assertEqual(templates, '{project_dir}/templates')
        self.assertEqual(my_prj_templates, '/code/lazy_format/tmps')
        self.assertEqual(my_prj_templates.format(project_dir='/develop'), '/develop/tmps')
        self.assertEqual(my_prj_templates.format(template_dir_name='templates2'), '/code/lazy_format/templates2')
