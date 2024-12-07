from app.exception.exceptions import LoxRuntimeException
from app.lexer.token import Token


class Environment:
    def __init__(self, env = None):
        self.values = {}
        self.hashSet = set({})
        self.enclosing = env
        
    def put(self, name: str, val):
        self.values[name] = val
        self.hashSet.add(name)
        
    def update(self, t: Token, val):
        name = t.lexeme
        if name not in self.hashSet:
            if self.enclosing == None:
                raise LoxRuntimeException(t, f"Undefined variable '{t.lexeme}'.")
            else:
                self.enclosing.update(t, val)
                return
        self.values[name] = val;
    
    def get(self, t: Token):
        if t.lexeme in self.hashSet:
            return self.values.get(t.lexeme)
        elif self.enclosing != None:
            return self.enclosing.get(t)    
        raise LoxRuntimeException(t, "Undefined variable '" + t.lexeme + "'.")
    