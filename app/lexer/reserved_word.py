from app.lexer.token import TokenTypes

class ReservedWord:
    reserved_words = {
        "and" : TokenTypes.AND,
        "class" : TokenTypes.CLASS,
        "else" : TokenTypes.ELSE,
        "false" : TokenTypes.FALSE,
        "for" : TokenTypes.FOR,
        "fun" : TokenTypes.FUN,
        "if" : TokenTypes.IF,
        "nil" : TokenTypes.NIL,
        "or" : TokenTypes.OR,
        "print" : TokenTypes.PRINT,
        "return": TokenTypes.RETURN,
        "super" : TokenTypes.SUPER,
        "this" : TokenTypes.THIS,
        "true" : TokenTypes.TRUE,
        "var" : TokenTypes.VAR,
        "while" : TokenTypes.WHILE,
        "lambda" : TokenTypes.LAMBDA
    }

    @staticmethod
    def isReservedWord(word: str):
        return ReservedWord.reserved_words.get(word) != None
    
    @staticmethod
    def extractType(word: str) -> TokenTypes:
        return ReservedWord.reserved_words.get(word)