from app.exception.exceptions import LoxRuntimeException
from app.exception.utils import reportRuntimeError
from app.lexer.token_types import TokenTypes
from app.lexer.token import Token


class Interpreter:
    def __init__(self, expr):
        self.expr = expr

    def evaluate(self):
        try:
            return self.expr.evaluateExpression()
        except LoxRuntimeException as e:
            reportRuntimeError(e)
            exit(70)


def getUnaryOp(t: Token):
    if t.type == TokenTypes.BANG:

        def f(a):
            # if type(a) != bool:
            #    raise LoxRuntimeException(t, "Operand must be a boolean.\n")
            return not a

        return f
    elif t.type == TokenTypes.MINUS:

        def f(a):
            if type(a) != int and type(a) != float:
                raise LoxRuntimeException(t, "Operand must be a number.\n")
            return -1 * a

        return f


def getBinaryOp(token: Token):
    if token.type == TokenTypes.PLUS:

        def f(x, y):
            if not (isBinaryNumber(x, y) or isBinaryString(x, y)):
                raise LoxRuntimeException(
                    token, "Operands must be two numbers or two strings.\n"
                )
            return x + y

        return f

    elif token.type == TokenTypes.MINUS:

        def f(x, y):
            if not isBinaryNumber(x, y):
                raise LoxRuntimeException(token, "Operands must be numbers.")
            return x - y

        return f

    elif token.type == TokenTypes.STAR:

        def times(x, y):
            if not isBinaryNumber(x, y):
                raise LoxRuntimeException(token, "Operands must be numbers.")
            return x * y

        return times

    elif token.type == TokenTypes.SLASH:

        def divide(x, y):
            if not isBinaryNumber(x, y):
                raise LoxRuntimeException(token, "Operands must be numbers.")
            if y == 0:
                raise LoxRuntimeException(token, "ZeroDivisionError")
            else:
                return x / y

        return divide

    elif token.type == TokenTypes.AND:
        return lambda x, y: x and y

    elif token.type == TokenTypes.OR:
        return lambda x, y: x or y

    elif token.type == TokenTypes.LESS:
        return lambda x, y: x < y

    elif token.type == TokenTypes.GREATER:
        return lambda x, y: x > y

    elif token.type == TokenTypes.LESS_EQUAL:
        return lambda x, y: x <= y

    elif token.type == TokenTypes.GREATER:
        return lambda x, y: x > y

    elif token.type == TokenTypes.GREATER_EQUAL:
        return lambda x, y: x >= y

    elif token.type == TokenTypes.EQUAL_EQUAL:
        return lambda x, y: x == y

    elif token.type == TokenTypes.BANG_EQUAL:
        return lambda x, y: x != y


def isBinaryNumber(x, y):
    return (type(x) == float or type(x) == int) and (type(y) == float or type(y) == int)


def isBinaryString(x, y):
    return type(x) == str and type(y) == str
