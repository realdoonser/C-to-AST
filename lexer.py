import ply.lex as lex
import sys
import re
# Tokens

reserved = {
    "if": "IF",
    "do": "DO",
    "else": "ELSE",
    "while": "WHILE",
    "for": "FOR",
    "int": "INT",
    "char": "CHAR",
    "void": "VOID",
    "short": "SHORT",
    "long": "LONG",
    "float": "FLOAT",
    "double": "DOUBLE",
    "return": "RETURN",
    "break": "BREAK",
    "continue": "CONTINUE",
    "struct": "STRUCT",
    "class": "CLASS",
}

literals = ['+', '-', '*', '/',
            '(', ')', '{', '}', '>', '<', ';', '=', '[', ']', '#', '.', ',', '?', ':', '|', '&']

assigneq_token = ['MULTEQ', 'DIVEQ', 'MODEQ', 'ADDEQ', 'SUBEQ']

logical_operator_token = ['LOGEQ', 'LOGNEQ', 'LOGOR', 'LOGAND']

bitwise_operator_token = ['LSHIFT', 'RSHIFT']

unary_operator_token = ['PLUSPLUS', 'MINUSMINUS', 'RARROW']

tokens = ["INCLUDE", "ID", "NUMBER", "GEQ", "LEQ", "STR",
          "CHR", ] + assigneq_token + logical_operator_token + bitwise_operator_token + unary_operator_token + list(reserved.values())

t_GEQ = r'>='
t_LEQ = r'<='
t_CHR = r"'.'"
t_STR = r'".*"'
t_MULTEQ = r'\*='
t_DIVEQ = r'/='
t_MODEQ = r'%='
t_ADDEQ = r'\+='
t_SUBEQ = r'-='
t_LOGNEQ = r'!='
t_LOGEQ = r'=='
t_LOGOR = r'\|\|'
t_LOGAND = r'&&'
t_LSHIFT = r'<<'
t_RSHIFT = r'>>'
t_PLUSPLUS = r'\+\+'
t_MINUSMINUS = r'--'
t_RARROW = r'->'


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t


def t_INCLUDE(t):
    r'\#include[ \t]*(?:<|")\w+\.\w+(?:>|")'
    t.value = re.search('(?:<|")\w+\.\w+(?:>|")', t.value).group()[1:-1]
    return t


def t_COMMENT(t):
    r'//.*'
    pass


def t_LONGCOMMENT(t):
    r'/\*(.|\n)*\*/'
    pass


def t_NUMBER(t):
    r'([0-9]+\.[0-9]*|[0-9]*\.[0-9]+|[0-9]+)'
    if ('.' in t.value):
        t.value = float(t.value)
    else:
        t.value = int(t.value)
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print("Invalid Token:", t.value[0])
    t.lexer.skip(1)


t_ignore = ' \t'


def make_lexer():
    lexer = lex.lex()
    return lexer


if __name__ == "__main__":
    with open(sys.argv[-1]) as f:
        data = f.read()
    lexer = make_lexer()
    lexer.input(data)
    for tok in lexer:
        print(tok)
