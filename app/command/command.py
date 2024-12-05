from app.interpreter.interpreter import Interpreter
from app.lexer.scanner import Scanner
from app.parser.parser import Parser
from app.expression import Empty
from app.interpreter.formatter import evaluateFormat
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
        expr_xs = p.parse()
        if type(expr_xs) == Empty:
            exit(65)
        for expr in expr_xs:
            print(expr.printExpression())

class Evaluate(Command):
    def __init__(self, content):
        super().__init__(content)
        self.shouldPrintFinal = False
        self.parseErrorCode = 70
    
    def execute(self):
        sc = self.scanner
        tokens, error = sc.scanTokens()
        if error:
            exit(65)
        p = Parser(tokens)
        expr = p.parse()
        if type(expr) == Empty:
            exit(self.parseErrorCode)
        int = Interpreter(expr)
        
        final = evaluateFormat(int.evaluate())
        if self.shouldPrintFinal:
            print(final)
    
class NormalEvaluate(Evaluate):
    def __init__(self, content):
        super().__init__(content)
        self.shouldPrintFinal = True
    
    def execute(self):
        return super().execute()
    
class RunEvaluate(Evaluate):
    def __init__(self, content):
        super().__init__(content)
        self.shouldPrintFinal = False
        self.parseErrorCode = 65
    
    def execute(self):
        return super().execute()