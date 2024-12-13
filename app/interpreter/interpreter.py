from app.environment.environment import Environment
from app.libraries.globals import global_table
from app.exception.exceptions import LoxRuntimeException
from app.exception.utils import reportRuntimeError
from app.syntax.statement import Statement

class Interpreter:
    def __init__(self, exprs : list[Statement], env: Environment):
        globalEnv = Environment()
        globalEnv.initializeTable(global_table)
        
        self.exprs = exprs
        self.environment = env
        self.environment.extend(globalEnv) 

    def evaluate(self):
        out = None
        try:
            for e in self.exprs:
                out = e.evaluateExpression(self.environment)
            return out
        except LoxRuntimeException as e:
            reportRuntimeError(e)
            exit(70)
            
    def traceEnv(self, env):
        if env == None:
            return 
        else:
            print(id(env), env.values)
            for e in env.children:
                self.traceEnv(e)