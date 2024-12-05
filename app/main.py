import sys
from app.lexer.scanner import Scanner
from app.parser.expression import Empty
from app.parser.parser import Parser

def scan(file_contents): 
    sc = Scanner(file_contents)
    return sc.scanTokens()[1]


def main(): 
    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    if command not in {"tokenize", "parse"}:
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)

    with open(filename) as file:
        file_contents = file.read()
    
    sc = Scanner(file_contents)
    if command == "tokenize":
        sc.shouldPrint = True
        error = sc.scanTokens()[1]
        if error:
            exit(65)
    elif command == "parse":
        tokens = sc.scanTokens()[0]
        error = sc.scanTokens()[1]
        if error:
            exit(65)
        p = Parser(tokens)
        expr = p.parse()
        if type(expr) == Empty:
            exit(65)
        print(expr.printExpression())
        

if __name__ == "__main__":
    main()
