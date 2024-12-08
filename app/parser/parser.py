from app.environment.environment import Environment
from app.exception.utils import reportError
from app.lexer.token import Token
from app.lexer.token_types import TokenTypes
from app.syntax.statement import (
    Assign,
    Empty,
    If,
    Literal,
    Binary,
    Expression,
    Logical,
    Statement,
    Unary,
    Grouping,
    PrintExpression,
    Var,
    Variable,
    Block,
    While,
)
from app.exception.exceptions import ParseException


class Parser:
    def __init__(self, tokens: list[Token], env: Environment):
        self.tokens = tokens
        self.current = 0
        self.env = env
        self.parseError = False

    def parseForEvaluate(self) -> list[Expression]:
        try:
            return [self.expression()]
        except ParseException:
            exit(65)

    def parseForRun(self) -> list[Statement]:
        statements = []
        while not self.isAtEnd():
            statements.append(self.declaration())
        return statements

    def block(self):
        statements = []
        while not self.check(TokenTypes.RIGHT_BRACE) and not self.isAtEnd():
            statements.append(self.declaration())
        self.consume(TokenTypes.RIGHT_BRACE, "Expect '}' after block.")
        return statements

    def declaration(self):
        try:
            if self.match(TokenTypes.VAR):
                return self.varDeclare()
            return self.statement()
        except ParseException:
            self.parseError = True
            return self.synchronize()

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
                return
            match self.peek().type:
                case TokenTypes.CLASS:
                    return
                case TokenTypes.FUN:
                    return
                case TokenTypes.VAR:
                    return
                case TokenTypes.PRINT:
                    return
            self.advance()
        return Empty()

    def statement(self):
        if self.match(TokenTypes.PRINT):
            return self.printStatement()
        elif self.match(TokenTypes.LEFT_BRACE):
            return Block(self.block())
        elif self.match(TokenTypes.IF):
            return self.ifStatement()
        elif self.match(TokenTypes.WHILE):
            return self.whileStatement()
        elif self.match(TokenTypes.FOR):
            return self.forStatement()
        return self.expressionStatement()
    
    def forStatement(self):
        self.consume(TokenTypes.LEFT_PAREN, "Expect '(' after for");
        
        if self.match(TokenTypes.SEMICOLON):
            initializer = None    
        elif self.match(TokenTypes.VAR):
            initializer = self.varDeclare()
        else:
            initializer = self.expressionStatement()
            
        condition = Literal(True) # vacuously true
        if not self.check(TokenTypes.SEMICOLON):
            condition = self.expression()
        self.consume(TokenTypes.SEMICOLON, "Expect ';' after loop condition")
        
        increment = None
        if not self.check(TokenTypes.RIGHT_PAREN):
            increment = self.expression()
        self.consume(TokenTypes.RIGHT_PAREN, "Expect ')' after clauses.")
        body = self.statement()
        
        if increment is not None:
            body = Block([body, increment])
        body = While(condition, body)
        
        if initializer is not None:
            body = Block([initializer, body])
        return body
        

    def ifStatement(self):
        self.consume(TokenTypes.LEFT_PAREN, "Expect '(' after if")
        condition = self.expression()
        self.consume(TokenTypes.RIGHT_PAREN, "Expect ')' after if condition")

        thenBranch = self.statement()
        elseBranch = None
        if self.match(TokenTypes.ELSE):
            elseBranch = self.statement()
        return If(condition, thenBranch, elseBranch)
    
    def whileStatement(self):
        self.consume(TokenTypes.LEFT_PAREN, "Expect '(' after while.")
        condition = self.expression()
        self.consume(TokenTypes.RIGHT_PAREN, "Expect ')' after condition")
        body = self.statement()
        return While(condition, body)

    def printStatement(self):
        expr = self.expression()
        self.consume(TokenTypes.SEMICOLON, 'Expect ";" after value')
        return PrintExpression(expr)

    def expressionStatement(self):
        expr = self.expression()
        self.consume(TokenTypes.SEMICOLON, 'Expect ";" after value')
        return expr

    def expression(self):
        return self.assignment()

    def assignment(self):
        expr = self.orOperation()

        if self.match(TokenTypes.EQUAL):
            equals = self.previous()
            value = self.assignment()
            if type(expr) == Variable:
                name = expr.name
                return Assign(name, value, self.env)
            else:
                self.error(equals, "Invalid assignment target")
        return expr

    def orOperation(self):
        expr = self.andOperation()

        while self.match(TokenTypes.OR):
            operator = self.previous()
            right = self.andOperation()
            expr = Logical(expr, operator, right)
        return expr

    def andOperation(self):
        expr = self.equality()

        while self.match(TokenTypes.AND):
            operator = self.previous()
            right = self.equality()
            expr = Logical(expr, operator, right)
        return expr

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
