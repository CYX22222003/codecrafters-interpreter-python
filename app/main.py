import sys
from app.command.command import Evaluate, Parse, Tokenize
from app.lexer.scanner import Scanner


def scan(file_contents):
    sc = Scanner(file_contents)
    return sc.scanTokens()[1]


def main():
    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    if command not in {"tokenize", "parse", "evaluate"}:
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)

    with open(filename) as file:
        file_contents = file.read()

    if command == "tokenize":
        c = Tokenize(file_contents)
    elif command == "parse":
        c = Parse(file_contents)
    elif command == "evaluate":
        c = Evaluate(file_contents)
    c.execute()


if __name__ == "__main__":
    main()
