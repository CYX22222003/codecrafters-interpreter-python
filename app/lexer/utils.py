from app.lexer.reserved_word import ReservedWord

def isValidIdentifierStart(char):
    return char == "_" or char.isalpha()


def isValidIdentifierBody(char):
    return char == "_" or char.isalnum()


def isReservedWord(word):
    return ReservedWord.isReservedWord(word)
