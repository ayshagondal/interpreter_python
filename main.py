import sys
class TokenType:
    AND = "AND"
    CLASS = "CLASS"
    ELSE = "ELSE"
    FALSE = "FALSE"
    FOR = "FOR"
    FUN = "FUN"
    IF = "IF"
    NIL = "NIL"
    OR = "OR"
    PRINT = "PRINT"
    RETURN = "RETURN"
    SUPER = "SUPER"
    THIS = "THIS"
    TRUE = "TRUE"
    VAR = "VAR"
    WHILE = "WHILE"

keywords = {
    "and": TokenType.AND,
    "class": TokenType.CLASS,
    "else": TokenType.ELSE,
    "false": TokenType.FALSE,
    "for": TokenType.FOR,
    "fun": TokenType.FUN,
    "if": TokenType.IF,
    "nil": TokenType.NIL,
    "or": TokenType.OR,
    "print": TokenType.PRINT,
    "return": TokenType.RETURN,
    "super": TokenType.SUPER,
    "this": TokenType.THIS,
    "true": TokenType.TRUE,
    "var": TokenType.VAR,
    "while": TokenType.WHILE,
}


class Token:
    def __init__(self, type, lexeme, literal, line):
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line
    def __str__(self):
        literal_str = "null" if self.literal is None else str(self.literal)
        return f"{self.type} {self.lexeme} {literal_str}"
class Scanner:
    def __init__(self, source):
        self.source = source
        self.start = 0
        self.current = 0
        self.line = 1
        self.errors = []
        self.tokens = []

    def scan_tokens(self):
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()
        self.tokens.append(Token("EOF", "", None, self.line))
        return self.tokens, self.errors
    
    def is_at_end(self):
        return self.current >= len(self.source)
    
    def scan_token(self):
        c = self.advance()
        if c == "(":
            self.add_token("LEFT_PAREN")
        elif c == ")":
            self.add_token("RIGHT_PAREN")
        elif c == "{":
            self.add_token("LEFT_BRACE")
        elif c == "}":
            self.add_token("RIGHT_BRACE")
        elif c == "*":
            self.add_token("STAR")
        elif c == ",":
            self.add_token("COMMA")
        elif c == ".":
            self.add_token("DOT")
        elif c == "+":
            self.add_token("PLUS")
        elif c == "-":
            self.add_token("MINUS")
        elif c == ";":
            self.add_token("SEMICOLON")
        elif c == "=":
            if self.match("="):
                self.add_token("EQUAL_EQUAL")
            else:
                self.add_token("EQUAL")
        elif c == ("!"):
            if self.match("="):
                self.add_token("BANG_EQUAL")
            else:
                self.add_token("BANG")
        elif c == "<":
            if self.match("="):
                self.add_token("LESS_EQUAL")
            else:
                self.add_token("LESS")
        elif c == ">":
            if self.match("="):
                self.add_token("GREATER_EQUAL")
            else:
                self.add_token("GREATER")
        elif c == "/":
            if self.match("/"):
                while self.peek() != "\n" and not self.is_at_end():
                    self.advance()
            else:
                self.add_token("SLASH")
        elif c == " ":
            pass
        elif c == "\n":
            self.line += 1
            pass
        elif c == "\t":
            pass
        elif c == "\r":
            pass
        elif c == '"':
            self.string()
            pass
        elif c == 'o':
            if self.match("r"):
                self.add_token("OR")
        
        else:
            if self.isDigit(c):
                self.number()
            elif self.isAlphaNumeric(c):
                self.identifier()
            else:
                self.error(f"Unexpected character: {c}")
    def identifier(self):
        while self.isAlphaNumeric(self.peek()):
            self.advance()

        text = self.source[self.start : self.current]
        token_type = keywords.get(text, "IDENTIFIER")
        self.add_token(token_type)

    def isAlpha(self, c):
        return c >= 'a' and c <= 'z' or c >= 'A' and c <= 'Z' or c == '_'
    def isAlphaNumeric(self, c):
        return self.isAlpha(c) or self.isDigit(c)
    
    def peek(self):
        if self.is_at_end():
            return "\0"
        return self.source[self.current]
    def match(self, expected):
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False
        self.current += 1
        return True
    
    def advance(self):
        self.current += 1
        return self.source[self.current - 1]
    
    def add_token(self, type, literal = None):
        text = self.source[self.start : self.current]
        self.tokens.append(Token(type, text, literal, self.line))

    def error(self, message):
        self.errors.append(f"[line {self.line}] Error: {message}")
    def string(self):
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == "\n":
                self.line += 1
            self.advance()
        if self.is_at_end():
            self.error("Unterminated string.")
            return
        self.advance()
        value = self.source[self.start + 1 : self.current - 1]
        self.add_token("STRING", value)
            
    def isDigit(self, c):
        return c >= '0' and c <= '9'
    def peek_next(self):
        if self.current + 1 >= len(self.source):
            return "\0"
        return self.source[self.current + 1]
    def number(self):
        while self.isDigit(self.peek()):
            self.advance()
        if self.peek() == "." and self.isDigit(self.peek_next()):
            self.advance()
        while self.isDigit(self.peek()):
            self.advance()
        self.add_token("NUMBER", float(self.source[self.start : self.current]))
            
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
       
    scanner = Scanner(file_contents)
    tokens, errors = scanner.scan_tokens()

    for token in tokens:
        print(token)

    for error in errors:
        print(error, file = sys.stderr)

    if errors:
        exit(65)




    
    print("Logs will appear here.", file=sys.stderr)

    

if __name__ == "__main__":
    main()
