from funvert import funvert, Funverted
import unittest

def incd(x, by=1):
    return x + by

def incremented(x, by=1):
    return x + by

class TestFunvert(unittest.TestCase):
    def test_is_callable_from_test_funvert(self):
        one = funvert(1)
        self.assertTrue(isinstance(one, Funverted))
        self.assertEqual(one._obj, 1)
        self.assertTrue(one.incd()._obj == 2)

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

    def test_can_use_plus_operator_after(self):
        one = funvert(1)
        two = one + 1
        self.assertEqual(two, 2)

    def test_can_use_plus_operator_before(self):
        one = funvert(1)
        two = 1 + one
        self.assertEqual(two, 2)

    def test_can_use_minus_operator_before(self):
        one = funvert(1)
        zero = one - 1
        self.assertEqual(zero, 0)

    def test_can_use_minus_operator_after(self):
        one = funvert(1)
        zero = 1 - one
        self.assertEqual(zero, 0)

    def test_can_use_multiply_operator_before(self):
        two = funvert(2)
        four = two * 2
        self.assertEqual(four, 4)

    def test_can_use_multiply_operator_after(self):
        two = funvert(2)
        four = 2 * two
        self.assertEqual(four, 4)

    def test_can_use_divide_operator_before(self):
        four = funvert(4)
        two = four / 2
        self.assertEqual(two, 2)

    def test_can_use_divide_operator_after(self):
        two = funvert(2)
        three = 6 / two
        self.assertEqual(three, 3)

    def test_can_use_floordiv_operator_before(self):
        five = funvert(5)
        two = five // 2
        self.assertEqual(two, 2)

    def test_can_use_floordiv_operator_after(self):
        two = funvert(2)
        two_again = 5 // two
        self.assertEqual(two_again, 2)

    def test_can_use_mod_operator_before(self):
        five = funvert(5)
        one = five % 2
        self.assertEqual(one, 1)

    def test_can_use_mod_operator_after(self):
        two = funvert(2)
        one = 5 % two
        self.assertEqual(one, 1)

    def test_can_use_parameter(self):
        one = funvert(1)
        three = one.incremented(2)
        self.assertEqual(three._obj, 3)

    def test_can_use_kwarg(self):
        one = funvert(1)
        three = one.incremented(by=2)
        self.assertEqual(three._obj, 3)

if __name__ == '__main__':
    unittest.main()
