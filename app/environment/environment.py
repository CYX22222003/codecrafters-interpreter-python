from app.environment.predefined import indexAt, makeList, scanin, toint, tostr, xsLength
from app.exception.exceptions import LoxRuntimeException
from app.lexer.token import Token
import time
import copy

from app.lexer.token_types import TokenTypes


class Environment:
    def __init__(self, env=None):
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
        self.values[name] = val

    def get(self, t: Token):
        if t.lexeme in self.hashSet:
            return self.values.get(t.lexeme)
        elif self.enclosing != None:
            return self.enclosing.get(t)
        raise LoxRuntimeException(t, "Undefined variable '" + t.lexeme + "'.")

    def extend(self, new_enclosse):
        self.enclosing = new_enclosse


class Global(Environment):
    def __init__(self):
        self.values = {
            "clock": lambda: time.time(),
            "scanin": scanin,
            "toint": toint,
            "tostr": tostr,
            "makeList": makeList,
            "indexAt": indexAt,
            "xsLength": xsLength,
        }
        self.hashSet = set(self.values.keys())
        self.enclosing = None
