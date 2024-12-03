import sys


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

    for line in file_contents:
            for char in line:
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
                        continue
                        # token = ""
                print(f"{token} {char} null")
    print("EOF  null")


if __name__ == "__main__":
    main()
