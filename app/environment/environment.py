from app.exception.exceptions import LoxRuntimeException
from app.lexer.token import Token


class Environment:
    def __init__(self):
        self.values = {}
        self.hashSet = set({})
        
    def put(self, name: str, val):
        self.values[name] = val
        self.hashSet.add(name)
    
    def get(self, t: Token):
        if t.lexeme in self.hashSet:
            return self.values.get(t.lexeme)
        raise LoxRuntimeException(t, "Undefined variable '" + t.lexeme + "'.")
    