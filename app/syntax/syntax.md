program        → declaration* EOF ;
declaration    → funDecl
               | varDecl
               | statement ;

funDecl        → "fun" function ;
function       → IDENTIFIER "(" parameters? ")" block;
parameters     → IDENTIFIER ("," parameters);

varDecl        → "var" IDENTIFIER ( "=" expression )? ";" ;

statement      → exprStmt
               | ifStmt
               | printStmt 
               | whileStmt
               | returnStmt
               | forStmt
               | block;

returnStmt     → "return" expression? ";"

forStmt        → "for" "(" (varDecl | exprStmt | ";") 
                expression? ";"
                expression?")" statement;
whileStmt      → "while" "(" expression ")" statement;
ifStmt         → "if" "(" expression ")" statement ("else" statement)?;
block          → "{" declaration* "}";
exprStmt       → expression ";" ;
printStmt      → "print" expression ";" ;

expression     → assignment;
assignment     → IDENTIFIER "=" assignment
               | logical_or;

logical_or     → logic_and ("or" logic_and)*
logic_and      → equality ("and" equality)* 
equality       → comparison ( ( "!=" | "==" ) comparison )* ;
comparison     → term ( ( ">" | ">=" | "<" | "<=" ) term )* ;
term           → factor ( ( "-" | "+" ) factor )* ;
factor         → unary ( ( "/" | "*" ) unary )* ;
unary          → ( "!" | "-" ) unary | call ;

call           → primary ("(" arguments? ")")*
arguments      → expression ( "," expression )*
primary        → NUMBER | STRING | "true" | "false" | "nil"
               | "(" expression ")" | IDENTIFIER | lambdaExpr;
lambdaExpr     → "lambda" "("parameters?")" (block | : expression);