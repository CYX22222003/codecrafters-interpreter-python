from app.lexer.token_types import TokenTypes
from app.lexer.token import Token

def getOpFunction(token: Token):
    if token.type == TokenTypes.PLUS:
        return lambda x, y: x + y
    
    elif token.type == TokenTypes.MINUS:
        return lambda x, y: x - y
    
    elif token.type == TokenTypes.STAR:
        return lambda x, y: x * y
    
    elif token.type == TokenTypes.SLASH:
        def divide(x, y):
            if y == 0:
                raise ZeroDivisionError()
            else:
                return x / y
        return divide
    
    elif token.type == TokenTypes.AND:
        return lambda x, y : x and y
    
    elif token.type == TokenTypes.OR:
        return lambda x, y: x or y
    
    elif token.type == TokenTypes.LESS:
        return lambda x, y : x < y
    
    elif token.type == TokenTypes.GREATER:
        return lambda x, y: x > y
    
    elif token.type == TokenTypes.LESS_EQUAL:
        return lambda x, y : x <= y
    
    elif token.type == TokenTypes.GREATER_EQUAL:
        return lambda x, y: x > y
    
    elif token.type == TokenTypes.EQUAL_EQUAL:
        return lambda x, y: x == y