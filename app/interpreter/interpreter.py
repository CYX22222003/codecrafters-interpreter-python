from app.environment.environment import Environment
from app.exception.exceptions import LoxRuntimeException
from app.exception.utils import reportRuntimeError
from app.program import Expression

class Interpreter:
    def __init__(self, exprs : list[Expression], env: Environment):
        self.exprs = exprs
        self.environment = env 

    def evaluate(self):
        out = None
        try:
            for e in self.exprs:
                out = e.evaluateExpression()
            return out
        except LoxRuntimeException as e:
            reportRuntimeError(e)
            exit(70)