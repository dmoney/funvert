# funvert.py
# A hack to enable calling functions as if they were methods
#
# Author: Dustin King (cathodion@gmail.com)
# Grown from this tweet by Zygmunt Zając:
#     https://twitter.com/zygmuntzajac/status/685161914117296128

class Funverted:
    def __init__(self, obj):
        self._obj=obj

    def __getattr__(self, name):
        try:
            return getattr(self._obj, name)
        except AttributeError:
            globprop = globals().get(name, None)
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
    def incd(x, by=1):
        return x + by
    fv = funvert
    print('7 ==', fv(1).incd().incd(2).incd(by=3))
    #=>  7 == 7

    #BUG:
    #print('8 ==', fv(1).incd().incd(2).incd(by=3) + 1)
    #TypeError: unsupported operand type(s) for +: 'Funverted' and 'int'
