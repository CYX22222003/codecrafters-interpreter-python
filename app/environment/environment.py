from app.exception.exceptions import LoxRuntimeException
from app.lexer.token import Token


class Environment:
    def __init__(self, env=None):
        self.values = {}
        self.hashSet = set({})
        self.enclosing = env
        self.children = []

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
        self.values[name] = val

    def get(self, t: Token):
        if t.lexeme in self.hashSet:
            return self.values.get(t.lexeme)
        elif self.enclosing != None:
            return self.enclosing.get(t)
        raise LoxRuntimeException(t, "Undefined variable '" + t.lexeme + "'.")

    def extend(self, new_enclosse):
        self.enclosing = new_enclosse
        new_enclosse.children.append(self)

    def initializeTable(self, tab):
        self.values = tab
        self.hashSet = set(self.values.keys())
