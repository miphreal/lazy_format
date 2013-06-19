# coding=utf-8


class Aliases(object):
    _aliases = {}  # shared attribute

    def __init__(self, context=None):
        self.context(context=context)

    def __getattr__(self, key):
        from lazy_format.format import LazyFormat

        if key in self._aliases:
            value = self._aliases[key]

            if isinstance(value, LazyFormat):
                return value.format(*self._runtime_context.args, **self._runtime_context.kwargs)

            if callable(value):
                return value(alias=key, context=self._runtime_context)

            return value

        raise AttributeError(key)

    @classmethod
    def add_alias(cls, alias, value):
        cls._aliases[alias] = value

    @classmethod
    def remove_alias(cls, alias):
        cls._aliases.pop(alias, None)

    @classmethod
    def clear_aliases(cls):
        cls._aliases.clear()

    def context(self, context=None):
        from lazy_format.context import Context
        self._runtime_context = context if context is not None else Context()
        return self


__all__ = ['Aliases']
