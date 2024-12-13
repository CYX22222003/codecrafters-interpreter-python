def convert_pyfunc(original):
    def f(*arguments):
        return original(*arguments)

    return f
