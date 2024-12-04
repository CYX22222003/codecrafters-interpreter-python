class Token:
    def __init__(self, type, lexeme, literal):
        self.type = type
        self.lexeme = lexeme
        self.literal = literal

    def __str__(self):
        return print(f"{self.type} {self.lexeme} {self.literal}")