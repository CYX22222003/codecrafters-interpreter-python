from abc import ABC, abstractmethod
from app.lexer.token import Token
class Expression(ABC):
    @abstractmethod
    def printExpression(self):
        pass
    
    def parathesis(*items):
        out = "("
        for i in items:
            out += (i + " ")
        out = out.strip()
        out += ")"
        return out
        
class Binary(Expression):
    def __init__(self, left: Expression, token: Token, right: Expression):
        self.left = left
        self.right = right
        self.token = token
        
    def printExpression(self):
        left_expr = self.left.printExpression()
        right_expr = self.right.printExpression()
        return Expression.parathesis(self.token.type.value, left_expr, right_expr)
    
class Literal(Expression):
    def __init__(self, literal: any):
        self.val = literal
        
    def printExpression(self):
        return str(self.val)
    
class Unary(Expression):
    def __init__(self, operator: Token, right: Expression):
        self.operator = operator
        self.right = right
        
    def printExpression(self):
        return super().parathesis(self.operator.token.type.value, self.right.printExpression())
    
class Grouping(Expression):
    def __init__(self, expr):
        self.expr = expr
        
    def printExpression(self):
        grp = self.expr.printExpression()
        return Expression.parathesis("grouping", grp)