import re

# ===================== Analisador Léxico =====================

# Definindo os tokens (ordem é importante!)
tokens = [
    ('KEYWORD', r'\b(if|else|int|float)\b'),  # Palavras reservadas
    ('NUMBER', r'\d+(\.\d*)?'),  # Números inteiros ou decimais
    ('ASSIGN', r'='),  # Atribuição (deve vir antes de OPERATOR)
    ('OPERATOR', r'[+\-*/<>]'),  # Operadores (excluindo '=')
    ('LPAREN', r'\('),  # Parêntese esquerdo
    ('RPAREN', r'\)'),  # Parêntese direito
    ('LBRACE', r'\{'),  # Chave esquerda
    ('RBRACE', r'\}'),  # Chave direita
    ('SEMICOLON', r';'),  # Ponto e vírgula
    ('IDENTIFIER', r'[a-zA-Z_]\w*'),  # Identificadores (deve vir depois de KEYWORD)
    ('WHITESPACE', r'\s+'),  # Espaços em branco (serão ignorados)
]

# Função para tokenizar a entrada
def lexer(input_code):
    token_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in tokens)
    for match in re.finditer(token_regex, input_code):
        kind = match.lastgroup
        value = match.group(kind)
        if kind != 'WHITESPACE':  # Ignorar espaços em branco
            yield (kind, value)

# ===================== Analisador Sintático =====================

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
                # Fim do bloco de código
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
        # Aceita expressões como: IDENTIFIER OPERATOR NUMBER
        # ou: NUMBER OPERATOR NUMBER
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
        self.match('KEYWORD')  # 'if'
        self.match('LPAREN')   # '('
        self.match('IDENTIFIER')  # Identificador (ex: 'x')
        self.match('OPERATOR')  # Operador de comparação (ex: '>')
        self.match('NUMBER')  # Número (ex: '0')
        self.match('RPAREN')  # ')'
        self.match('LBRACE')  # '{'
        self.program()  # Bloco de código dentro do if
        self.match('RBRACE')  # '}'

    def match(self, expected_kind):
        if self.current_token and self.current_token[0] == expected_kind:
            self.next_token()
        else:
            raise SyntaxError(f"Expected {expected_kind}, got {self.current_token}")

# ===================== Exemplos de Uso =====================

# Exemplo 1: Declaração de variável e expressão
input_code1 = "int x = 10; x = x + 5;"
print("Tokens para o código 1:")
for token in lexer(input_code1):
    print(token)

print("\nAnálise sintática para o código 1:")
tokens1 = lexer(input_code1)
parser1 = Parser(tokens1)
parser1.parse()
print("Análise sintática concluída com sucesso!")

# Exemplo 2: Condicional
input_code2 = "if (x > 0) { x = x - 1; }"
print("\nTokens para o código 2:")
for token in lexer(input_code2):
    print(token)

print("\nAnálise sintática para o código 2:")
tokens2 = lexer(input_code2)
parser2 = Parser(tokens2)
parser2.parse()
print("Análise sintática concluída com sucesso!")

# Exemplo 3: Declaração de variável float
input_code3 = "float y = 3.14;"
print("\nTokens para o código 3:")
for token in lexer(input_code3):
    print(token)

print("\nAnálise sintática para o código 3:")
tokens3 = lexer(input_code3)
parser3 = Parser(tokens3)
parser3.parse()
print("Análise sintática concluída com sucesso!")