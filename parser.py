import ply.yacc as yacc
from lexer import tokens
import sys
import pprint


# precedence = (
#     ('left', '+', '-'),
#     ('left', '*', '/'),
#     ('right', 'UMINUS'),
#     ('right', 'LPLUS', 'LMINUS')
# )


class n:
    def __init__(self, type, children=[], info=None) -> None:
        self.type = type
        self.children = children
        self.info = info

    def __repr__(self) -> str:
        return pprint.pformat({"type": self.type, "children": self.children, "info": self.info}, width=500, sort_dicts=False)


def p_program(p):
    """
        program : include program
                | external_decl program
                | include
                | external_decl
    """
    if (len(p) == 3):
        # has program
        p[0] = n("program", [p[1]] + p[2].children)
    elif (len(p) == 2):
        p[0] = n("program", [p[1]])
    else:
        raise "Error at program"


def p_include(p):
    """
        include : INCLUDE
    """
    p[0] = n("include", [], p[1])


def p_external_declaration(p):
    """
        external_decl   : type ID ';'
                        | type ID '=' NUMBER ';'
                        | type ID '=' CHR ';'
    """
    var = n("var", [], (p[1].type, p[2]))
    if (len(p) == 6):
        num = n("num", [], (p[4]))
        p[0] = n("assign", [var, num])
    elif (len(p) == 4):
        p[0] = n("decl", [var])


def p_type(p):
    """
        type    : VOID 
                | CHAR 
                | SHORT 
                | INT 
                | LONG 
                | FLOAT 
                | DOUBLE
    """
    p[0] = n(p[1])


parser = yacc.yacc()

if __name__ == "__main__":
    with open(sys.argv[-1]) as f:
        data = f.read()
    result: n = parser.parse(data)
    print(result)
