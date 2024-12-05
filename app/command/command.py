from app.lexer.scanner import Scanner
from app.parser.parser import Parser
from app.parser.expression import Empty
from app.parser.formatter import evaluateFormat
from abc import ABC, abstractmethod


class Command(ABC):
    def __init__(self, content):
        self.content = content
        self.scanner = Scanner(content)

    @abstractmethod
    def execute(self):
        pass


class Tokenize(Command):
    def __init__(self, content):
        super().__init__(content)

    def execute(self):
        sc = self.scanner
        sc.shouldPrint = True
        error = sc.scanTokens()[1]
        if error:
            exit(65)


class Parse(Command):
    def __init__(self, content):
        super().__init__(content)
    
    def execute(self):
        sc = self.scanner
        tokens, error = sc.scanTokens()
        if error:
            exit(65)
        p = Parser(tokens)
        expr = p.parse()
        if type(expr) == Empty:
            exit(65)
        print(expr.printExpression())

class Evaluate(Command):
    def __init__(self, content):
        super().__init__(content)
    
    def execute(self):
        sc = self.scanner
        tokens, error = sc.scanTokens()
        if error:
            exit(65)
        p = Parser(tokens)
        expr = p.parse()
        if type(expr) == Empty:
            exit(65)
        print(evaluateFormat(expr.evaluateExpression()))
    