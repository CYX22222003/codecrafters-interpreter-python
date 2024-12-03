import sys

def scan(file_contents):
    error = False
    index = 0
    while index < len(file_contents):
        char = file_contents[index]
        shouldPrint = True
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
            case "!":
                next = index + 1
                if next < len(file_contents) and file_contents[next] == "=":
                    token = "BANG_EQUAL"
                    index = next
                else:
                    token = "BANG"
            case "=":
                next = index + 1
                if next < len(file_contents) and file_contents[next] == "=":
                    token = "EQUAL_EQUAL"
                    index = next
                else:
                    token = "EQUAL"
            case "<":
                next = index + 1
                if next < len(file_contents) and file_contents[next] == "=":
                    token = "LESS_EQUAL"
                    index = next
                else:
                    token = "LESS"
            case ">":
                next = index + 1
                if next < len(file_contents) and file_contents[next] == "=":
                    token = "GREATER_EQUAL"
                    index = next
                else:
                    token = "GREATER"
            case _:
                error = True
                shouldPrint = False
                line_number = (
                    file_contents.count("\n", 0, file_contents.find(char)) + 1
                )
                print(
                    f"[line {line_number}] Error: Unexpected character: {char}",
                    file=sys.stderr,
                )
        
        if shouldPrint:
            print(f"{token} {char} null")
        
        index += 1
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
