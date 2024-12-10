from app.environment.environment import Environment, Global
from app.exception.exceptions import LoxRuntimeException
from app.exception.utils import reportRuntimeError
from app.syntax.statement import Expression, Statement

class Interpreter:
    def __init__(self, exprs : list[Statement], env: Environment):
        self.exprs = exprs
        self.environment = env
        self.environment.extend(Global()) 

    def evaluate(self):
        out = None
        try:
            for e in self.exprs:
                out = e.evaluateExpression(self.environment)
            return out
        except LoxRuntimeException as e:
            reportRuntimeError(e)
            exit(70)