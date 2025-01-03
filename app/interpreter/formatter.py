def evaluateFormat(value):
    if type(value) == bool:
        return 'true' if value else 'false'      
    if value is None:
        return 'nil'
    if type(value) == float and value.is_integer():
        return int(value)
    if callable(value):
        return f"<fn {value.__name__}>"
    return value