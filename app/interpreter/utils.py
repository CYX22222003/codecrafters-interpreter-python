from app.exception.exceptions import LoxRuntimeException
from app.exception.utils import reportRuntimeError
from app.lexer.token_types import TokenTypes
from app.lexer.token import Token

MUST_BE_NUMBER = "Operand must be a number\n"
MUST_BE_NUMBERS = "Operands must be two numbers\n"
MUST_BE_BINARY_NUMBERS_OR_STRINGS = "Operands must be two numbers or two strings.\n"


def getUnaryOp(t: Token):
    if t.type == TokenTypes.BANG:

        def f(a):
            return not a

        return f
    elif t.type == TokenTypes.MINUS:

        def f(a):
            if type(a) != int and type(a) != float:
                raise LoxRuntimeException(t, MUST_BE_NUMBER)
            return -1 * a

        return f


def getBinaryOp(token: Token):
    if token.type == TokenTypes.PLUS:

        def f(x, y):
            if not (isBinaryNumber(x, y) or isBinaryString(x, y)):
                raise LoxRuntimeException(token, MUST_BE_BINARY_NUMBERS_OR_STRINGS)
            return x + y

        return f

    elif token.type == TokenTypes.MINUS:

        def f(x, y):
            if not isBinaryNumber(x, y):
                raise LoxRuntimeException(token, MUST_BE_NUMBERS)
            return x - y

        return f

    elif token.type == TokenTypes.STAR:

        def times(x, y):
            if not isBinaryNumber(x, y):
                raise LoxRuntimeException(token, MUST_BE_NUMBERS)
            return x * y

        return times

    elif token.type == TokenTypes.SLASH:

        def divide(x, y):
            if not isBinaryNumber(x, y):
                raise LoxRuntimeException(token, MUST_BE_NUMBERS)
            if y == 0:
                raise LoxRuntimeException(token, "ZeroDivisionError")
            else:
                return x / y

        return divide

    elif token.type == TokenTypes.LESS:

        def f(x, y):
            if not isBinaryNumber(x, y):
                raise LoxRuntimeException(token, MUST_BE_NUMBERS)
            return x < y

        return f

    elif token.type == TokenTypes.GREATER:

        def f(x, y):
            if not isBinaryNumber(x, y):
                raise LoxRuntimeException(token, MUST_BE_NUMBERS)
            return x > y

        return f

    elif token.type == TokenTypes.LESS_EQUAL:

        def f(x, y):
            if not isBinaryNumber(x, y):
                raise LoxRuntimeException(token, MUST_BE_NUMBERS)
            return x <= y

        return f

    elif token.type == TokenTypes.GREATER:

        def f(x, y):
            if not isBinaryNumber(x, y):
                raise LoxRuntimeException(token, MUST_BE_NUMBERS)
            return x > y

        return f

    elif token.type == TokenTypes.GREATER_EQUAL:

        def f(x, y):
            if not isBinaryNumber(x, y):
                raise LoxRuntimeException(token, MUST_BE_NUMBERS)
            return x >= y

        return f

    elif token.type == TokenTypes.EQUAL_EQUAL:
        return lambda x, y: x == y

    elif token.type == TokenTypes.BANG_EQUAL:
        return lambda x, y: x != y


def isBinaryNumber(x, y):
    return (type(x) == float or type(x) == int) and (type(y) == float or type(y) == int)


def isBinaryString(x, y):
    return type(x) == str and type(y) == str

def isTruthy(x):
    return x != False and x != None