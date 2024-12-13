from abc import ABC, abstractmethod
from typing import Iterable
from app.environment.environment import Environment
from app.exception.exceptions import LoxRuntimeException, ReturnException
from app.lexer.token import Token
from app.interpreter.utils import getBinaryOp, getUnaryOp, isTruthy
from app.interpreter.formatter import evaluateFormat
from app.lexer.token_types import TokenTypes

class Statement(ABC):
    @abstractmethod
    def evaluateExpression(self, env=None):
        pass


class Expression(Statement):
    @abstractmethod
    def printExpression(self):
        pass

    def parathesis(*items):
        out = "("
        for i in items:
            out += i + " "
        out = out.strip()
        out += ")"
        return out


class While(Statement):
    def __init__(self, condition: Expression, body: Statement):
        self.condition = condition
        self.body = body

    def evaluateExpression(self, env=None):
        out = None
        while isTruthy(self.condition.evaluateExpression(env)):
            out = self.body.evaluateExpression(env)
        return out


class Function(Statement):
    def __init__(self, name: Token, params: list[Token], body: list[Statement]):
        self.name = name
        self.params = params
        self.body = body 
    
    def evaluateExpression(self, env=None):
        def f(*args):
            curEnv = Environment()
            curEnv.extend(env)
            if len(args) != len(self.params):
                raise TypeError("Wrong number of parameters")
            
            for i in range(len(args)):
                curEnv.put(self.params[i].lexeme, args[i])

            out = Empty()
            bodyEnv = Environment()
            bodyEnv.extend(curEnv)
            
            try:
                for b in self.body:
                    out = b.evaluateExpression(bodyEnv)
            except ReturnException as r:
                out = r.value.evaluateExpression(bodyEnv)
            return out
        
        env.put(self.name.lexeme, f)
        f.__name__ = self.name.lexeme
        return

class LambdaExpr(Expression):
    def __init__(self, params: list[Token], body: list[Statement]):
        self.params = params
        self.body = body
        
    def printExpression(self):
        return Expression.parathesis("lambda", self.parathesis(self.params))
    
    def evaluateExpression(self, env=None):
        def f(*args):
            curEnv = Environment()
            curEnv.extend(env)
            if len(args) != len(self.params):
                raise TypeError("Wrong number of parameters")
            
            for i in range(len(args)):
                curEnv.put(self.params[i].lexeme, args[i])

            out = Empty()
            bodyEnv = Environment()
            bodyEnv.extend(curEnv)
            
            if type(self.body) is not list:
                out = self.body.evaluateExpression(bodyEnv)
                return out
            
            try:
                for b in self.body:
                    out = b.evaluateExpression(bodyEnv)
            except ReturnException as r:
                out = r.value.evaluateExpression(bodyEnv)
            return out
        return f
    
    
        
class Return(Statement):
    def __init__(self, keyword: Token, value: Expression):        
        self.keyword = keyword
        self.value = value
        
    def evaluateExpression(self, env=None):
        raise ReturnException(self.value)
        
        
        
class If(Statement):
    def __init__(
        self, condition: Expression, thenBranch: Statement, elseBranch: Statement
    ):
        self.condition = condition
        self.thenBranch = thenBranch
        self.elseBranch = elseBranch

    def evaluateExpression(self, env):
        if self.condition.evaluateExpression(env):
            return self.thenBranch.evaluateExpression(env)
        elif self.elseBranch is not None:
            return self.elseBranch.evaluateExpression(env)
        else:
            return


class Block(Statement):
    def __init__(self, statements: list[Expression]):
        self.statements = statements
        self.currentEnv = Environment()

    def evaluateExpression(self, env=None):
        self.currentEnv.extend(env)
        out = None
        for statement in self.statements:
            out = statement.evaluateExpression(self.currentEnv)
        return out


class Var(Statement):
    def __init__(self, name: Token, identifier: Expression, env: Environment):
        self.name = name
        self.identifier = identifier
        self.env = env

    def evaluateExpression(self, env):
        env.put(self.name.lexeme, self.identifier.evaluateExpression(env))


class PrintExpression(Statement):
    def __init__(self, expr):
        self.expr = expr

    def evaluateExpression(self, env):
        print(evaluateFormat(self.expr.evaluateExpression(env)))
        return


class Logical(Expression):
    def __init__(self, left: Expression, operator: Token, right: Expression):
        self.left = left
        self.operator = operator
        self.right = right

    def printExpression(self):
        return super().printExpression()

    def evaluateExpression(self, env=None):
        leftCond = self.left.evaluateExpression(env)
        if self.operator.type == TokenTypes.OR:
            if isTruthy(leftCond):
                return leftCond
            return self.right.evaluateExpression(env)
        else:
            if not isTruthy(leftCond):
                return leftCond
            return self.right.evaluateExpression(env)


class Assign(Expression):
    def __init__(self, name: Token, value: Expression, env: Environment):
        self.name = name
        self.val = value
        self.env = env

    def evaluateExpression(self, env):
        val = self.val.evaluateExpression(env)
        env.update(self.name, val)
        return val

    def printExpression(self):
        return Expression.parathesis(
            "assign", self.name.lexeme, self.val.printExpression()
        )


class Variable(Expression):
    def __init__(self, name: Token, env: Environment):
        self.name = name
        self.env = env

    def evaluateExpression(self, env):
        return env.get(self.name)

    def printExpression(self):
        return Expression.parathesis("identifier", self.name.lexeme)


class Binary(Expression):
    def __init__(self, left: Expression, token: Token, right: Expression):
        self.left = left
        self.right = right
        self.token = token

    def printExpression(self):
        left_expr = self.left.printExpression()
        right_expr = self.right.printExpression()
        return Expression.parathesis(self.token.type.value, left_expr, right_expr)

    def evaluateExpression(self, env):
        left = self.left.evaluateExpression(env)
        right = self.right.evaluateExpression(env)
        func = getBinaryOp(self.token)
        return func(left, right)


class Literal(Expression):
    def __init__(self, literal: any):
        self.val = literal

    def printExpression(self):
        if type(self.val) == bool:
            return str(self.val).lower()
        elif self.val == None:
            return "nil"
        return str(self.val)

    def evaluateExpression(self, env=None):
        return self.val


class Unary(Expression):
    def __init__(self, operator: Token, right: Expression):
        self.operator = operator
        self.right = right

    def printExpression(self):
        return Expression.parathesis(
            self.operator.type.value, self.right.printExpression()
        )

    def evaluateExpression(self, env):
        f = getUnaryOp(self.operator)
        right = self.right.evaluateExpression(env)
        return f(right)


class Grouping(Expression):
    def __init__(self, expr):
        self.expr = expr

    def printExpression(self):
        grp = self.expr.printExpression()
        return Expression.parathesis("group", grp)

    def evaluateExpression(self, env):
        return self.expr.evaluateExpression(env)


class Empty(Expression):
    def printExpression(self):
        return ""

    def evaluateExpression(self, env):
        return super().evaluateExpression(env)


class Call(Expression):
    def __init__(self, callee: Expression, paren: Token, arguments: list[Expression]):
        self.callee = callee
        self.paren = paren
        self.arguments = arguments

    def printExpression(self):
        return super().printExpression()

    def evaluateExpression(self, env=None):
        curEnv = Environment()
        curEnv.extend(env)
        f = self.callee.evaluateExpression(curEnv)
        arguments = []
        for expr in self.arguments:
            arguments.append(expr.evaluateExpression(curEnv))
        if not callable(f):
            raise LoxRuntimeException(
                self.paren,
                f"Can only call functions and classes. Received type {type(f)}",
            )

        try:
            out = f(*arguments)
        except TypeError as e:
            raise LoxRuntimeException(self.paren, str(e))
        return out
