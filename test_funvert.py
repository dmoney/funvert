from funvert import funvert, Funverted
import unittest

def incd(x, by=1):
    return x + by

class TestFunvert(unittest.TestCase):
    def test_is_callable_from_test_funvert(self):
        one = funvert(1)
        self.assertTrue(isinstance(one, Funverted))
        self.assertEqual(one._obj, 1)
        self.assertTrue(one.incd()._obj == 2)

if __name__ == '__main__':
    unittest.main()
