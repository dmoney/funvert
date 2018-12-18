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

def funvert(obj):
    if isinstance(obj, Funverted):
        return obj
    else:
        return Funverted(obj)


if __name__ == '__main__':
    from test_funvert import TestFunvert
    import unittest

    def incremented(x, by=1):
        return x + by

    class TestFunvertLocal(unittest.TestCase):
        def test_funvert_produces_funverted(self):
            one = funvert(1)
            self.assertTrue(isinstance(one, Funverted))

        def test_obj_is_original(self):
            original_one = 1
            one = funvert(original_one)
            self.assertTrue(one._obj is original_one)

        def test_function_callable_as_method(self):
            one = funvert(1)
            two = one.incremented()
            self.assertEqual(two._obj, 2)

        def test_regular_method_callable(self):
            class Dog:
                def bark(self):
                    return 'Woof!'
            dog = funvert(Dog())
            sound = dog.bark()
            self.assertEqual(sound, 'Woof!')

        def test_regular_property_gettable(self):
            class Dog:
                def __init__(self):
                    self.furry = True

                def bark(self):
                    return 'Woof!'

            dog = funvert(Dog())
            furry = dog.furry
            self.assertTrue(furry)

        def test_doesnt_double_funvert(self):
            one = funvert(1)
            one_prime = funvert(one)
            self.assertTrue(one is one_prime)

        # def test_can_use_operator_afterward(self):
        #     one = funvert(1)
        #     two = one + 1
        #     self.assertEqual(two._obj, 2)
        #
        # def test_can_use_operator_before(self):
        #     one = funvert(1)
        #     two = 1 + one
        #     self.assertEqual(two._obj, 2)

        def test_can_use_parameter(self):
            one = funvert(1)
            three = one.incremented(2)
            self.assertEqual(three._obj, 3)

        def test_can_use_kwarg(self):
            one = funvert(1)
            three = one.incremented(by=2)
            self.assertEqual(three._obj, 3)

    unittest.main()
