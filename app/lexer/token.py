from app.lexer.token_types import TokenTypes

class Token:
    def __init__(self, type: TokenTypes, lexeme: str, literal: str):
        self.type = type
        self.lexeme = lexeme
        self.literal = literal

    def __str__(self):
        return f"{self.type.name} {self.lexeme} {self.literal}"