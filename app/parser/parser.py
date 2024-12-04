from app.lexer.token import Token
from app.lexer.token_types import TokenTypes
from app.parser.expression import Literal, Binary, Expression, Unary, Grouping
import sys

class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.current = 0
    
    def parse(self) -> Expression:
        return self.expression()
    
    def expression(self):
        return self.equality()
    
    def equality(self) -> Expression:
        # print("check equality")
        expr = self.comparison()
        while (self.match(TokenTypes.BANG_EQUAL, TokenTypes.EQUAL_EQUAL)):
            opr = self.previous()
            right = self.comparison()
            expr = Binary(expr, opr, right)
        return expr
    
    def comparison(self) -> Expression:
        expr = self.term()
        while self.match(TokenTypes.GREATER, TokenTypes.GREATER_EQUAL, TokenTypes.LESS, TokenTypes.LESS_EQUAL):
            opr = self.previous()
            right = self.term()
            expr = Binary(expr, opr, right)
        return expr
    
    def term(self) -> Expression:
        expr = self.factor()
        while (self.match(TokenTypes.MINUS, TokenTypes.PLUS)):
            opr = self.previous()
            right = self.factor()
            expr = Binary(expr, opr, right)
        return expr
    
    def factor(self) -> Expression:
        expr = self.unary()
        
        while self.match(TokenTypes.SLASH, TokenTypes.STAR):
            opr = self.previous()
            right = self.unary()
            expr = Binary(expr, opr, right)
        return expr
    
    def unary(self) -> Expression:
        if self.match(TokenTypes.BANG, TokenTypes.MINUS):
            opr = self.previous()
            right = self.unary()
            return Unary(opr, right)
        return self.primary()
    
    def primary(self):
        if self.match(TokenTypes.FALSE):
            return Literal("false")
        elif self.match(TokenTypes.TRUE):
            return Literal("true")
        elif self.match(TokenTypes.NIL):
            return Literal("nil")
        
        elif self.match(TokenTypes.NUMBER, TokenTypes.STRING):
            return Literal(self.previous().literal)
        
        elif self.match(TokenTypes.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenTypes.RIGHT_PAREN, "Error")
            return Grouping(expr)
    
    def consume(self, token, msg):
        if self.check(token):
            self.advance()
        print(msg, file=sys.stderr)
            
    def match(self, *types) -> bool:
        for type in types:
            if self.check(type):
                self.advance()
                return True
        return False
    
    def check(self, type: TokenTypes) -> bool:
        if self.isAtEnd():
            return False
        return self.peek().type == type
    
    def peek(self) -> Token:
        return self.tokens[self.current]
    
    def isAtEnd(self) -> bool:
        return self.peek().type == TokenTypes.EOF
    
    def advance(self) -> Token:
        if (not self.isAtEnd()):
            self.current += 1
        return self.previous()
    
    def previous(self) -> Token:
        return self.tokens[self.current - 1]
    
    
        