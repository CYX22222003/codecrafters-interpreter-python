from app.token import Token
import sys


class Scanner:
    def __init__(self, source):
        self.source = source
        self.tokens = []
        self.upper = len(source)
        self.pointer = 0
        self.errorStatus = False

    def isAtEnd(self):
        return self.pointer >= self.upper

    def scanTokens(self):
        while not self.isAtEnd():
            self.scanToken()
        self.tokens.append(Token("EOF", "", "null"))
        print(Token("EOF", "", "null"))
        return (self.tokens, self.errorStatus)

    def scanToken(self):
        char = self.source[self.pointer]
        shouldPrint = True
        literal = "null"
        if char in {"(", ")", "{", "}", ",", ".", "-", "+", ";", "*"}:
            self.processNormal(char)
        elif char in {"!", ">", "=", "<"}:
            self.processEquality(char)
        elif char == "/":
            self.processSlash(char)
        elif char in {"\t", " ", "\n"}:
            pass
        elif char == '"':
            self.processString(char)
        elif char.isdigit():
            self.processNumber(char)
        elif Scanner.isValidIdentifierStart(char):
            self.processAlpha(char)
        else:
            self.errorStatus = True
            self.generateErrorMsg(char)
        self.pointer += 1

    def printAndAddToken(self, token, lexeme, literal):
        t = Token(token, lexeme, literal)
        print(t)
        self.tokens.append(t)

    def generateUnclosedString(self):
        line_number = self.source.count("\n", 0, self.pointer) + 1
        print(
            f"[line {line_number}] Error: Unterminated string.",
            file=sys.stderr,
        )

    def generateErrorMsg(self, char):
        line_number = self.source.count("\n", 0, self.pointer) + 1
        print(
            f"[line {line_number}] Error: Unexpected character: {char}",
            file=sys.stderr,
        )

    def processNormal(self, char):
        literal = "null"
        if char == "(":
            token = "LEFT_PAREN"
        elif char == ")":
            token = "RIGHT_PAREN"
        elif char == "{":
            token = "LEFT_BRACE"
        elif char == "}":
            token = "RIGHT_BRACE"
        elif char == ",":
            token = "COMMA"
        elif char == ".":
            token = "DOT"
        elif char == "-":
            token = "MINUS"
        elif char == "+":
            token = "PLUS"
        elif char == ";":
            token = "SEMICOLON"
        elif char == "*":
            token = "STAR"
        self.printAndAddToken(token, char, literal)

    def processEquality(self, char):
        literal = "null"
        if char == "!":
            next = self.pointer + 1
            if next < len(self.source) and self.source[next] == "=":
                token = "BANG_EQUAL"
                char = "!="
                self.pointer = next
            else:
                token = "BANG"
        elif char == "=":
            next = self.pointer + 1
            if next < len(self.source) and self.source[next] == "=":
                token = "EQUAL_EQUAL"
                char = "=="
                self.pointer = next
            else:
                token = "EQUAL"
        elif char == "<":
            next = self.pointer + 1
            if next < len(self.source) and self.source[next] == "=":
                token = "LESS_EQUAL"
                char = "<="
                self.pointer = next
            else:
                token = "LESS"
        elif char == ">":
            next = self.pointer + 1
            if next < len(self.source) and self.source[next] == "=":
                token = "GREATER_EQUAL"
                char = ">="
                self.pointer = next
            else:
                token = "GREATER"

        self.printAndAddToken(token, char, literal)

    def processSlash(self, char):
        literal = "null"
        next = self.pointer + 1
        if next < len(self.source) and self.source[next] == "/":
            while next < len(self.source) and self.source[next] != "\n":
                next += 1
            self.pointer = next
        else:
            token = "SLASH"
            self.printAndAddToken(token, char, literal)

    def processString(self, char):
        next = self.pointer + 1
        isClose = False
        while next < len(self.source):
            char += self.source[next]
            if self.source[next] == '"':
                isClose = True
                break
            next += 1

        self.pointer = next
        if not isClose:
            self.errorStatus = True
            self.generateUnclosedString()
        else:
            token = "STRING"
            literal = char[1 : len(char) - 1]
            self.printAndAddToken(token, char, literal)

    def processNumber(self, char):
        self.pointer += 1
        while self.pointer < len(self.source) and self.source[self.pointer].isdigit():
            char += self.source[self.pointer]
            self.pointer += 1

        if self.pointer < len(self.source) and self.source[self.pointer] == ".":
            char += self.source[self.pointer]
            self.pointer += 1
        
        while self.pointer < len(self.source) and self.source[self.pointer].isdigit():
            char += self.source[self.pointer]
            self.pointer += 1

        self.pointer -= 1
        token = "NUMBER"
        literal = float(char)

        self.printAndAddToken(token, char, literal)
        
    def processAlpha(self, char):
        self.pointer += 1
        while (not self.isAtEnd()) and Scanner.isValidIdentifierBody(self.source[self.pointer]):
            char += self.source[self.pointer]
            self.pointer += 1
            
        token = "IDENTIFIER"
        literal = "null"
        self.printAndAddToken(token, char, literal)
        
    @staticmethod
    def isValidIdentifierStart(char):
        return char == "_" or char.isalpha()
    
    @staticmethod
    def isValidIdentifierBody(char):
        return char == "_" or char.isalnum()
