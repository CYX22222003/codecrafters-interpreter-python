import sys

from app.exception.exceptions import LoxRuntimeException

def reportError(line: int, where: str, msg: str):
    print(f"[line {line}] Error{where}: {msg}", file=sys.stderr)
    
def reportRuntimeError(err : LoxRuntimeException):
    print(f"{str(err)}[line {err.token.line}]", file=sys.stderr)
    