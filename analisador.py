import re

tokens = [
    ('KEYWORD', r'\b(if|else|int|float)\b'),  
    ('NUMBER', r'\d+(\.\d*)?'),  
    ('ASSIGN', r'='), 
    ('OPERATOR', r'[+\-*/<>]'), 
    ('LPAREN', r'\('),  
    ('RPAREN', r'\)'),  
    ('LBRACE', r'\{'),  
    ('RBRACE', r'\}'), 
    ('SEMICOLON', r';'),
    ('IDENTIFIER', r'[a-zA-Z_]\w*'),
    ('WHITESPACE', r'\s+'),
]

def lexer(input_code):
    token_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in tokens)
    for match in re.finditer(token_regex, input_code):
        kind = match.lastgroup
        value = match.group(kind)
        if kind != 'WHITESPACE':  
            yield (kind, value)


class Parser:
    def __init__(self, tokens):
        self.tokens = list(tokens)
        self.current_token = None
        self.next_token()

    def next_token(self):
        if self.tokens:
            self.current_token = self.tokens.pop(0)
        else:
            self.current_token = None

    def parse(self):
        self.program()

    def program(self):
        while self.current_token:
            if self.current_token[0] == 'KEYWORD' and self.current_token[1] in ['int', 'float']:
                self.declaration()
            elif self.current_token[0] == 'IDENTIFIER':
                self.assignment()
            elif self.current_token[0] == 'KEYWORD' and self.current_token[1] == 'if':
                self.conditional()
            elif self.current_token[0] == 'RBRACE':
             
                break
            else:
                raise SyntaxError(f"Unexpected token: {self.current_token}")

    def declaration(self):
        self.match('KEYWORD')
        self.match('IDENTIFIER')
        self.match('ASSIGN')
        self.match('NUMBER')
        self.match('SEMICOLON')

    def assignment(self):
        self.match('IDENTIFIER')
        self.match('ASSIGN')
        self.expression()
        self.match('SEMICOLON')

    def expression(self):

        if self.current_token[0] in ['IDENTIFIER', 'NUMBER']:
            self.next_token()
            self.match('OPERATOR')
            if self.current_token[0] in ['IDENTIFIER', 'NUMBER']:
                self.next_token()
            else:
                raise SyntaxError(f"Expected IDENTIFIER or NUMBER, got {self.current_token}")
        else:
            raise SyntaxError(f"Expected IDENTIFIER or NUMBER, got {self.current_token}")

    def conditional(self):
        self.match('KEYWORD')  
        self.match('LPAREN')   
        self.match('IDENTIFIER') 
        self.match('OPERATOR')  
        self.match('NUMBER') 
        self.match('RPAREN')  
        self.match('LBRACE')  
        self.program()  
        self.match('RBRACE') 

    def match(self, expected_kind):
        if self.current_token and self.current_token[0] == expected_kind:
            self.next_token()
        else:
            raise SyntaxError(f"Expected {expected_kind}, got {self.current_token}")


input_code1 = "int x = 10; x = x + 5;"
print("Tokens para o código 1:")
for token in lexer(input_code1):
    print(token)

print("\nAnálise sintática para o código 1:")
tokens1 = lexer(input_code1)
parser1 = Parser(tokens1)
parser1.parse()
print("Análise sintática concluída com sucesso!")

input_code2 = "if (x > 0) { x = x - 1; }"
print("\nTokens para o código 2:")
for token in lexer(input_code2):
    print(token)

print("\nAnálise sintática para o código 2:")
tokens2 = lexer(input_code2)
parser2 = Parser(tokens2)
parser2.parse()
print("Análise sintática concluída com sucesso!")

input_code3 = "float y = 3.14;"
print("\nTokens para o código 3:")
for token in lexer(input_code3):
    print(token)

print("\nAnálise sintática para o código 3:")
tokens3 = lexer(input_code3)
parser3 = Parser(tokens3)
parser3.parse()
print("Análise sintática concluída com sucesso!")