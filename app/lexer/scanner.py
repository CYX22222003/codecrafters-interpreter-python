from app.exception.utils import reportError
from app.lexer.token import Token
from app.lexer.reserved_word import ReservedWord
from app.lexer.token_types import TokenTypes
from app.lexer.utils import (
    isValidIdentifierBody,
    isValidIdentifierStart,
    isReservedWord,
    countLine,
)


class Scanner:
    def __init__(self, source, shouldPrint=False):
        self.source = source
        self.tokens = []
        self.upper = len(source)
        self.pointer = 0
        self.errorStatus = False
        self.shouldPrint = shouldPrint

    def isAtEnd(self):
        return self.pointer >= self.upper

    def scanTokens(self):
        while not self.isAtEnd():
            self.scanToken()
        self.tokens.append(
            Token(TokenTypes.EOF, "", "null", countLine(self.source, 0, self.pointer) - 2)
        )
        if self.shouldPrint:
            print(
                Token(
                    TokenTypes.EOF, "", "null", countLine(self.source, 0, self.pointer) - 2
                )
            )
        return (self.tokens, self.errorStatus)

    def scanToken(self):
        char = self.source[self.pointer]
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
        elif isValidIdentifierStart(char):
            self.processAlpha(char)
        else:
            self.errorStatus = True
            self.generateErrorMsg(char)
        self.pointer += 1

    def printAndAddToken(self, token, lexeme, literal):
        t = Token(token, lexeme, literal, countLine(self.source, 0, self.pointer))
        if self.shouldPrint:
            print(t)
        self.tokens.append(t)

    def generateUnclosedString(self):
        line_number = countLine(self.source, 0, self.pointer)
        reportError(line_number, "", "Unterminated String.")

    def generateErrorMsg(self, char):
        line_number = countLine(self.source, 0, self.pointer)
        reportError(line_number, "", f"Unexpeceted character: {char}")

    def processNormal(self, char):
        literal = "null"
        if char == "(":
            token = TokenTypes.LEFT_PAREN
        elif char == ")":
            token = TokenTypes.RIGHT_PAREN
        elif char == "{":
            token = TokenTypes.LEFT_BRACE
        elif char == "}":
            token = TokenTypes.RIGHT_BRACE
        elif char == ",":
            token = TokenTypes.COMMA
        elif char == ".":
            token = TokenTypes.DOT
        elif char == "-":
            token = TokenTypes.MINUS
        elif char == "+":
            token = TokenTypes.PLUS
        elif char == ";":
            token = TokenTypes.SEMICOLON
        elif char == "*":
            token = TokenTypes.STAR
        self.printAndAddToken(token, char, literal)

    def processEquality(self, char):
        literal = "null"
        if char == "!":
            next = self.pointer + 1
            if next < len(self.source) and self.source[next] == "=":
                token = TokenTypes.BANG_EQUAL
                char = "!="
                self.pointer = next
            else:
                token = TokenTypes.BANG
        elif char == "=":
            next = self.pointer + 1
            if next < len(self.source) and self.source[next] == "=":
                token = TokenTypes.EQUAL_EQUAL
                char = "=="
                self.pointer = next
            else:
                token = TokenTypes.EQUAL
        elif char == "<":
            next = self.pointer + 1
            if next < len(self.source) and self.source[next] == "=":
                token = TokenTypes.LESS_EQUAL
                char = "<="
                self.pointer = next
            else:
                token = TokenTypes.LESS
        elif char == ">":
            next = self.pointer + 1
            if next < len(self.source) and self.source[next] == "=":
                token = TokenTypes.GREATER_EQUAL
                char = ">="
                self.pointer = next
            else:
                token = TokenTypes.GREATER
        self.printAndAddToken(token, char, literal)

    def processSlash(self, char):
        literal = "null"
        next = self.pointer + 1
        if next < len(self.source) and self.source[next] == "/":
            while next < len(self.source) and self.source[next] != "\n":
                next += 1
            self.pointer = next
        else:
            token = TokenTypes.SLASH
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
            token = TokenTypes.STRING
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
        token = TokenTypes.NUMBER
        literal = float(char)

        self.printAndAddToken(token, char, literal)

    def processAlpha(self, char):
        self.pointer += 1
        while (not self.isAtEnd()) and isValidIdentifierBody(self.source[self.pointer]):
            char += self.source[self.pointer]
            self.pointer += 1

        self.pointer -= 1
        if isReservedWord(char):
            token = ReservedWord.extractType(char)
            literal = "null"
        else:
            token = TokenTypes.IDENTIFIER
            literal = "null"
        self.printAndAddToken(token, char, literal)

    def getTokens(self):
        return self.tokens
