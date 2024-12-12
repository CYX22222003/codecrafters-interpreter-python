import time

from app.exception.exceptions import LoxRuntimeException
def clock():
    return time.time()

def scanin(msg):
    return convert_pyfunc(input)(msg)

def toint(a):
    return convert_pyfunc(int)(a)
    
def tostr(a):
    return convert_pyfunc(str)(a)

def makeList(*a):
    xs = []
    for i in a:
        xs.append(i)
    return xs

def indexAt(xs, ind):
    original = lambda x, ind: x[int(ind)]
    return convert_pyfunc(original)(xs, ind)

def xsLength(xs):
    return convert_pyfunc(len)(xs)
    
def convert_pyfunc(original):
    def f(*arguments):
        return original(*arguments)
    return f