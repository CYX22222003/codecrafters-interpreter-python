from abc import ABC, abstractmethod
from app.lexer.token import Token
from app.parser.interpreter import getOpFunction

class Expression(ABC):
    @abstractmethod
    def printExpression(self):
        pass

    @abstractmethod
    def evaluateExpression(self):
        pass
    
    def parathesis(*items):
        out = "("
        for i in items:
            out += (i + " ")
        out = out.strip()
        out += ")"
        return out
    
    def getOp(token: Token):
        return getOpFunction(token)
        
class Binary(Expression):
    def __init__(self, left: Expression, token: Token, right: Expression):
        self.left = left
        self.right = right
        self.token = token
        
    def printExpression(self):
        left_expr = self.left.printExpression()
        right_expr = self.right.printExpression()
        return Expression.parathesis(self.token.type.value, left_expr, right_expr)
    
    def evaluateExpression(self):
        left = self.left.evaluateExpression()
        right = self.right.evaluateExpression()
        func = Expression.getOp(self.token)
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
    
    def evaluateExpression(self):
        return self.val
    
class Unary(Expression):
    def __init__(self, operator: Token, right: Expression):
        self.operator = operator
        self.right = right
        
    def printExpression(self):
        return Expression.parathesis(self.operator.type.value, self.right.printExpression())
    
    def evaluateExpression(self):
        pass
    
class Grouping(Expression):
    def __init__(self, expr):
        self.expr = expr
        
    def printExpression(self):
        grp = self.expr.printExpression()
        return Expression.parathesis("group", grp)
    
    def evaluateExpression(self):
        return super().evaluateExpression()
    
class Empty(Expression):
    def printExpression(self):
        return ""
    
    def evaluateExpression(self):
        return super().evaluateExpression()