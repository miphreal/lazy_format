## lazy_format

[![Build Status](https://travis-ci.org/miphreal/lazy_format.png?branch=master)](https://travis-ci.org/miphreal/lazy_format)

Simple way to have partially applied formatted strings.

This python package provides a wrapper around the 'str.format' functionality in order to skip unresolved formatting parts.
All arguments are applied lazily.


## Install

Enter the following command:

```bash
  $ pip install lazy_format
```


## Examples

More examples you can find in the [tests](../../tree/master/tests).

Common use case:
```python
>>> from lazy_format import LazyFormat
>>>
>>> lazy = LazyFormat('{0} {1} {0} {msg} {var1} {var2} {obj!r} {x:.2f}', 'fist arg', msg='Hello')
>>> lazy
<lazy_format.format.LazyFormat at 0x22a2590>
>>> print lazy
fist arg {1} fist arg Hello {var1} {var2} {obj!r} {x:.2f}
>>>
>>> lazy.format('second arg', obj=LazyFormat, x=22/7.)
"fist arg second arg fist arg Hello {var1} {var2} <class 'lazy_format.format.LazyFormat'> 3.14"
>>>
>>> lazy.format('second arg', obj=LazyFormat, x=22/7., var1='1', var2=2)
"fist arg second arg fist arg Hello 1 2 <class 'lazy_format.format.LazyFormat'> 3.14"
>>>
>>> lazy.format('second arg', obj=LazyFormat, x=22/7., var1='1', var2=2, msg='Bye')
"fist arg second arg fist arg Bye 1 2 <class 'lazy_format.format.LazyFormat'> 3.14"
```

Global context:
```python
>>> LazyFormat.global_context.update_context_with({'global_var1': 'GV1', 'global_var2': 'GV2'})
>>> lazy2 = LazyFormat('{global_var1}, {global_var2}')
>>> print lazy2
GV1, GV2
>>> print lazy2.format(global_var1='my var1')
my var1, GV2
```

Extra features:
```python
>>> from lazy_format import Aliases
>>> from lazy_format import LazyAliasFormat
>>>
>>> Aliases.add_alias('project_name', 'LazyFormat')
>>> lazy3 = LazyAliasFormat('{alias.project_name}')
>>> print lazy3
LazyFormat
>>>
>>>
>>> def func(alias, context):
>>>     return 'dyn value for ' + alias
>>>
>>> Aliases.add_alias('val', func)
>>> lazy4 = LazyAliasFormat('{alias.val}')
>>> print lazy4
dyn value for val
>>>
>>>
>>> LazyAliasFormat('{project_dir}', alias='dir')
<lazy_format.format.LazyAliasFormat at 0x22a2a50>
>>> templates = LazyAliasFormat('{alias.dir}/{template_dir_name}',
>>>                             template_dir_name='templates',
>>>                             alias='template_dir')
>>>
>>> my_prj_templates = LazyAliasFormat('{alias.template_dir}',
>>>                                    project_dir='/code/lazy_format',
>>>                                    template_dir_name='tmps')
>>> print templates
{project_dir}/templates
>>> print my_prj_templates
/code/lazy_format/tmps
>>> print my_prj_templates.format(project_dir='/code2')
/code2/tmps
```





