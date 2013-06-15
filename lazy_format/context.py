# coding=utf-8
from itertools import chain


class Context(object):
    def __init__(self, args=None, context=None):
        self._args_spaces = []
        self._context_spaces = []

        self.add_args(tuple(args) if args is not None else ())
        self.update_context_with(context if context is not None else {})

    @property
    def args(self):
        return tuple(chain(*self._args_spaces))

    @property
    def kwargs(self):
        ctx = {}
        for c in reversed(self._context_spaces):
            ctx.update(c)
        return ctx

    def add_args(self, args):
        self._args_spaces.append(tuple(args))

    def update_context_with(self, context, update_initial=False):
        if not update_initial:
            self._context_spaces.insert(0, context.copy())
        else:
            self._context_spaces[-1].update(context)

    def clear(self, save_initial=True):
        if save_initial:
            del self._args_spaces[1:]
            del self._context_spaces[:-1]
        else:
            del self._args_spaces[:]
            del self._context_spaces[:]


__all__ = ['Context']