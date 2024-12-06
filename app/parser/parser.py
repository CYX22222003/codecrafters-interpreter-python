from app.environment.environment import Environment
from app.exception.utils import reportError
from app.lexer.token import Token
from app.lexer.token_types import TokenTypes
from app.program import (
    Empty,
    Literal,
    Binary,
    Expression,
    Unary,
    Grouping,
    PrintExpression,
    Var,
    Variable,
)
from app.exception.exceptions import ParseException


class Parser:
    def __init__(self, tokens: list[Token], env: Environment):
        self.tokens = tokens
        self.current = 0
        self.env = env

    def parseForEvaluate(self) -> list[Expression]:
        try:
            return [self.expression()]
        except ParseException:
            exit(65)

    def parseForRun(self) -> list[Expression]:
        statements = []
        try:
            while not self.isAtEnd():
                statements.append(self.declaration())
            return statements
        except ParseException:
            exit(65)
            # return Empty()

    def declaration(self):
        try:
            if self.match(TokenTypes.VAR):
                return self.varDeclare()
            return self.statement()
        except ParseException:
            self.synchronize()
            # exit(65)

    def varDeclare(self):
        name = self.consume(TokenTypes.IDENTIFIER, "Expect variable name.")
        initializer = None
        if self.match(TokenTypes.EQUAL):
            initializer = self.expression()
        else:
            initializer = Literal(None)
        self.consume(TokenTypes.SEMICOLON, "Expect ';' after variable declaration")
        return Var(name, initializer, self.env)

    def synchronize(self):
        self.advance()
        while not self.isAtEnd():
            if self.previous().type == TokenTypes.SEMICOLON:
                return Empty()
            if self.peek().type == TokenTypes.RETURN:
                return Empty()
            self.advance()

    def statement(self):
        if self.match(TokenTypes.PRINT):
            return self.printStatement()
        return self.expressionStatement()

    def printStatement(self):
        expr = self.expression()
        self.consume(TokenTypes.SEMICOLON, 'Expect ";" after value')
        return PrintExpression(expr)

    def expressionStatement(self):
        expr = self.expression()
        self.consume(TokenTypes.SEMICOLON, 'Expect ";" after value')
        return expr

    def expression(self):
        return self.equality()

    def equality(self) -> Expression:
        expr = self.comparison()
        while self.match(TokenTypes.BANG_EQUAL, TokenTypes.EQUAL_EQUAL):
            opr = self.previous()
            right = self.comparison()
            expr = Binary(expr, opr, right)
        return expr

    def comparison(self) -> Expression:
        expr = self.term()
        while self.match(
            TokenTypes.GREATER,
            TokenTypes.GREATER_EQUAL,
            TokenTypes.LESS,
            TokenTypes.LESS_EQUAL,
        ):
            opr = self.previous()
            right = self.term()
            expr = Binary(expr, opr, right)
        return expr

    def term(self) -> Expression:
        expr = self.factor()
        while self.match(TokenTypes.MINUS, TokenTypes.PLUS):
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

    def primary(self) -> Expression:
        if self.match(TokenTypes.FALSE):
            return Literal(False)
        elif self.match(TokenTypes.TRUE):
            return Literal(True)
        elif self.match(TokenTypes.NIL):
            return Literal(None)
        elif self.match(TokenTypes.IDENTIFIER):
            return Variable(self.previous(), self.env)
        elif self.match(TokenTypes.NUMBER, TokenTypes.STRING):
            return Literal(self.previous().literal)

        elif self.match(TokenTypes.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenTypes.RIGHT_PAREN, "Expect ')' after expression.")
            return Grouping(expr)
        else:
            raise self.error(self.peek(), "Expect expression.")

    def consume(self, token: Token, msg: str):
        if self.check(token):
            return self.advance()
        else:
            raise self.error(self.peek(), msg)

    def error(self, token: Token, msg: str) -> ParseException:
        if token.type == TokenTypes.EOF:
            reportError(token.line, " at end", msg)
        else:
            reportError(token.line, f" at '{token.lexeme}'", msg)
        return ParseException()

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
        if not self.isAtEnd():
            self.current += 1
        return self.previous()

    def previous(self) -> Token:
        return self.tokens[self.current - 1]
