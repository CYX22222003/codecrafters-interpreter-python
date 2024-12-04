import sys
from app.scanner import Scanner

def scan(file_contents): 
    sc = Scanner(file_contents)
    return sc.scanTokens()[1]

def main(): 
    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    if command != "tokenize":
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)

    with open(filename) as file:
        file_contents = file.read()

    error = scan(file_contents=file_contents)
    if error:
        exit(65)

if __name__ == "__main__":
    main()
