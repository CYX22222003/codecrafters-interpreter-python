from app.exception.exceptions import LoxRuntimeException
from app.lexer.token import Token


class Environment:
    def __init__(self):
        self.values = {}
        
    def put(self, name: str, val):
        self.values[name] = val
    
    def get(self, t: Token):
        if self.values.get(t.lexeme) != None:
            return self.values.get(t.lexeme)
        
        raise LoxRuntimeException(t, "Undefined variable '" + t.lexeme + "'.")
    