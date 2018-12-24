# funvert.py
# A hack to enable calling functions as if they were methods
#
# Author: Dustin King (cathodion@gmail.com)
# Grown from this tweet by Zygmunt Zając:
#     https://twitter.com/zygmuntzajac/status/685161914117296128

import inspect

def stackFrameContext(depth):
    context = {}

    # depth + 1 because 0 is the context of the calling function
    frame = inspect.stack()[depth + 1].frame

    # add global and local variables from the appropriate context
    context.update(frame.f_globals)
    context.update(frame.f_locals)

    return context

class Funverted:
    def __init__(self, obj):
        self._obj=obj

    def __getattr__(self, name):
        try:
            return getattr(self._obj, name)
        except AttributeError:
            globprop = stackFrameContext(1).get(name, None)
            if callable(globprop):
                return lambda *args, **kwargs: funvert(globprop(self._obj, *args, **kwargs))
            else:
                raise

    def __str__(self):
        return str(self._obj)

    def __add__(self, rhs):
        return self._obj + rhs

    def __radd__(self, lhs):
        return lhs + self._obj

def funvert(obj):
    if isinstance(obj, Funverted):
        return obj
    else:
        return Funverted(obj)


if __name__ == '__main__':
    from test_funvert import TestFunvert
    import unittest

    unittest.main()
