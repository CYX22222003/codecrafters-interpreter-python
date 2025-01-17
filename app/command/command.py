from app.environment.environment import Environment
from app.interpreter.interpreter import Interpreter
from app.lexer.scanner import Scanner
from app.parser.parser import Parser
from app.syntax.statement import Empty
from app.interpreter.formatter import evaluateFormat
from abc import ABC, abstractmethod


class Command(ABC):
    def __init__(self, content):
        self.content = content
        self.scanner = Scanner(content)
        self.environment = Environment()

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
        p = Parser(tokens, self.environment)
        if p.parseError:
            exit(65)
        expr_xs = p.parseForEvaluate()
        for expr in expr_xs:
            print(expr.printExpression())

class Evaluate(Command):
    def __init__(self, content):
        super().__init__(content)
        self.shouldPrintFinal = False
    
    @abstractmethod
    def execute(self):
        pass
    
class NormalEvaluate(Evaluate):
    def __init__(self, content):
        super().__init__(content)
        self.shouldPrintFinal = True
    
    def execute(self):
        sc = self.scanner
        tokens, error = sc.scanTokens()
        if error:
            exit(65)
        p = Parser(tokens, self.environment)
        expr_xs = p.parseForEvaluate()
        int = Interpreter(expr_xs, self.environment)
        
        final = evaluateFormat(int.evaluate())
        if self.shouldPrintFinal:
            print(final) 
    
class RunEvaluate(Evaluate):
    def __init__(self, content):
        super().__init__(content)
        self.shouldPrintFinal = False
    
    def execute(self):
        sc = self.scanner
        tokens, error = sc.scanTokens()
        if error:
            exit(65)
        p = Parser(tokens, self.environment)
        expr = p.parseForRun()
        if p.parseError:
            exit(65)
        int = Interpreter(expr, self.environment)
        
        final = evaluateFormat(int.evaluate())
        if self.shouldPrintFinal:
            print(final)