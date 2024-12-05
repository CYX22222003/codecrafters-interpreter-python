from app.exception.exceptions import LoxRuntimeException
from app.exception.utils import reportRuntimeError

class Interpreter:
    def __init__(self, exprs):
        self.exprs = exprs

    def evaluate(self):
        out = None
        try:
            for e in self.exprs:
                out = e.evaluateExpression()
            return out
        except LoxRuntimeException as e:
            reportRuntimeError(e)
            exit(70)