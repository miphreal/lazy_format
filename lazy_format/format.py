# coding=utf-8
"""
Provides some classes that allow to manipulate the context data flexibly and
get lazy object that renders itself only if it's used as a string.
"""

from aliases import Aliases
from context import Context
from formatter import LazyFormatter


class LazyFormat(object):

    _formatter = LazyFormatter()

    # shared attribute
    # uses the kwargs (context) functionality of the Context class only
    global_context = Context()

    def __init__(self, text, *partial_args, **partial_context):
        self._text = text
        self._context = Context(partial_args, dict(self.global_context.kwargs, **partial_context))

    def context(self, args, kwargs):
        self._context.clear()
        self._context.add_args(args)
        self._context.update_context_with(kwargs)
        return self._context

    def format(self, *args, **kwargs):
        context = self.context(args, kwargs)
        return self._formatter.format(self._text, *context.args, **context.kwargs)

    __format__ = __unicode__ = __str__ = format

    def __add__(self, other):
        return u'{0!s}{1!s}'.format(self, other)

    def __eq__(self, other):
        return self.format() == other

    def __ne__(self, other):
        return self.format() != other

    def __len__(self):
        return len(self.format())


class LazyAliasFormat(LazyFormat):
    CONTEXT_ALIAS_NAMESPACE = 'alias'

    def __init__(self, text, *partial_args, **partial_context):
        alias = partial_context.pop('alias', None)

        super(LazyAliasFormat, self).__init__(text, *partial_args, **partial_context)

        self._alias = alias
        self._aliases = Aliases()

        if self._alias:
            self._aliases.add_alias(alias, self)

    def context(self, args, kwargs):
        context = super(LazyAliasFormat, self).context(args=args, kwargs=kwargs)
        context.update_context_with({
            self.CONTEXT_ALIAS_NAMESPACE: self._aliases.context(context)
        })
        return context


__all__ = ['LazyAliasFormat' , 'LazyFormat']