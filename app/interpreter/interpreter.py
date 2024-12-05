from app.exception.exceptions import LoxRuntimeException
from app.exception.utils import reportRuntimeError

class Interpreter:
    def __init__(self, expr):
        self.expr = expr

    def evaluate(self):
        try:
            return self.expr.evaluateExpression()
        except LoxRuntimeException as e:
            reportRuntimeError(e)
            exit(70)