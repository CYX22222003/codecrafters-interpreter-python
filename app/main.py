import sys

def scan(file_contents):
    error = False
    for char in file_contents:
        error = False
        match char:
            case "(":
                token = "LEFT_PAREN"
            case ")":
                token = "RIGHT_PAREN"
            case "{":
                token = "LEFT_BRACE"
            case "}":
                token = "RIGHT_BRACE"
            case ",":
                token = "COMMA"
            case ".":
                token = "DOT"
            case "-":
                token = "MINUS"
            case "+":
                token = "PLUS"
            case ";":
                token = "SEMICOLON"
            case "*":
                token = "STAR"
            case _:
                error = True
                line_number = (
                    file_contents.count("\n", 0, file_contents.find(char)) + 1
                )
                print(
                    f"[line {line_number}] Error: Unexpected character: {char}",
                    file=sys.stderr,
                )
        if not error:
            print(f"{token} {char} null")
    print("EOF  null")
    return error

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
