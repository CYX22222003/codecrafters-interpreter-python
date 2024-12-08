from abc import ABC, abstractmethod
from app.environment.environment import Environment
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
    def __init__(self, left : Expression, operator: Token, right: Expression):
        self.left = left
        self.operator = operator
        self.right = right
        
    def printExpression(self):
        return super().printExpression();
    
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
