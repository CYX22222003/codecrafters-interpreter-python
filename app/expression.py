from abc import ABC, abstractmethod
from app.token import Token
class Expression(ABC):
    @abstractmethod
    def form(self):
        pass
        
class Binary(Expression):
    def __init__(self, left: Expression, right: Expression, token: Token):
        self.left = left
        self.right = right
        self.token = token