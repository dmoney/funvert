# funvert
Function Inverter

Methods are just functions, therefore we should be able to call functions as though they were methods.

This is accomplished by:

* The `Funverted` class, which wraps the original object and overloads `__getattr__()` to look for functions
* The `funvert()` function, which is the recommended way to wrap and prevents double-wrapping
* the ._obj property, which gives the unwrapped object if needed.


Example:

```python
from funvert import funvert as fv

def incd(x, by=1):
    return x + by

print('7 ==', fv(1).incd().incd(2).incd(by=3))
#=>  7 == 7

# this changes the type, so operators like + don't work currently.
# print('8 ==', fv(1).incd().incd(2).incd(by=3) + 1)
# ==> TypeError: unsupported operand type(s) for +: 'Funverted' and 'int'

# use ._obj to get the plain type object
print('8 ==', fv(1).incd().incd(2).incd(by=3),_obj + 1)
#=> 8 == 8
```

A funverted object still has its own methods available:

```python
class Dog:
    def bark(self):
        print('Woof!')

d = fv(Dog())
d.bark()
#=> Woof!
```

One day all classes will inherit from Funverted and bound methods will be a thing of the past!

That day is not today.  Inheriting from Funverted is not currently supported, and calling a function in this way often creates a new `Funverted` object, which may impose a performance penalty.

### THERE IS CURRENTLY A SERIOUS BUG PREVENTING FUNVERT FROM BEING USED OUTSIDE funvert.py ITSELF.
[See Issue 1](https://github.com/dmoney/funvert/issues/1).
This is being evolved from a gist, so it is not ready for production use yet.  The only way to use it currently is to copy/paste funvert() and Funverted into the same file or REPL session.
