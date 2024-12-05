import sys
def reportError(line: int, where: str, msg: str):
    print(f"[line {line}] Error{where}: {msg}", file=sys.stderr)