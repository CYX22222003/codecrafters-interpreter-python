import sys

def scan(file_contents):
    error = False
    for char in file_contents:
        match char:
            case "(":
                token = "LEFT_PAREN"
                print(f"{token} {char} null")
            case ")":
                token = "RIGHT_PAREN"
                print(f"{token} {char} null")
            case "{":
                token = "LEFT_BRACE"
                print(f"{token} {char} null")
            case "}":
                token = "RIGHT_BRACE"
                print(f"{token} {char} null")
            case ",":
                token = "COMMA"
                print(f"{token} {char} null")
            case ".":
                token = "DOT"
                print(f"{token} {char} null")
            case "-":
                token = "MINUS"
                print(f"{token} {char} null")
            case "+":
                token = "PLUS"
                print(f"{token} {char} null")
            case ";":
                token = "SEMICOLON"
                print(f"{token} {char} null")
            case "*":
                token = "STAR"
                print(f"{token} {char} null")
            case _:
                error = True
                line_number = (
                    file_contents.count("\n", 0, file_contents.find(char)) + 1
                )
                print(
                    f"[line {line_number}] Error: Unexpected character: {char}",
                    file=sys.stderr,
                )
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
