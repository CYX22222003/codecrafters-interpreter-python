import time
from app.libraries.converter import convert_pyfunc


def clock():
    return time.time()


def scanin(msg):
    return convert_pyfunc(input)(msg)


def toint(a):
    return convert_pyfunc(int)(a)


def tostr(a):
    return convert_pyfunc(str)(a)
