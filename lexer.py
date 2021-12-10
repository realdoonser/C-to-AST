import ply.lex as lex

# Tokens

reserved = {
    "if": "IF",
    "then": "THEN",
    "else": "ELSE",
    "while": "WHILE",
}

tokens = ["NAME", "NUMBER", "PLUS", "MINUS",
          "TIMES", "DIVIDE", "EQUALS", "LPAREN", "RPAREN", "LBRACE", "RBRACE", "SEMICOLON", "ID"] + list(reserved.values())

t_PLUS = r'\+'
t_MINUS = r'\-'
t_TIMES = r'\*'
t_DIVIDE = r'\/'
t_EQUALS = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_SEMICOLON = r';'


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t


def t_NUMBER(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print("Invalid Token:", t.value[0])
    t.lexer.skip(1)


def t_COMMENT(t):
    r'\#.*'
    pass


t_ignore = ' \t'

lexer = lex.lex()
