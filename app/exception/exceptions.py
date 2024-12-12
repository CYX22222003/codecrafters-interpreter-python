class ParseException(Exception):
    pass

class LoxRuntimeException(Exception):
    def __init__(self, token, message):
        super().__init__(message)
        self.message = message
        self.token = token
        
    def __str__(self):
        return self.message
    
class ReturnException(Exception):
    def __init__(self, value):
        self.value = value