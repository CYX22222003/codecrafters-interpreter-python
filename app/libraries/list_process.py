from app.libraries.converter import convert_pyfunc


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


def updateIndex(xs, ind, target):
    def original(xs, ind, target):
        xs[int(ind)] = target

    return convert_pyfunc(original)(xs, ind, target)


def appendEle(xs, ele):
    return convert_pyfunc((lambda xs, ele: xs.append(ele)))(xs, ele)
