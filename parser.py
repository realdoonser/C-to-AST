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

# =========== For the whole program ===========


def p_program(p):
    """
        program : include program
                | external_decl program
    """
    p[0] = n("program", [p[1]] + p[2].children)


def p_program_end(p):
    """
        program : include
                | external_decl
    """
    p[0] = n("program", [p[1]])

# ----------------- program end -------------------

# =================== include =====================


def p_include(p):
    """
        include : INCLUDE
    """
    p[0] = n("include", [], p[1])

# ---------------- include end -------------------


def p_external_declaration(p):
    """
        external_decl   : decl
    """
    p[0] = n("external_decl", [p[1]])


def p_decl(p):
    """
        decl : type declarators ';'
    """
    p[0] = n("decl", [p[2]], (p[1],))


def p_decl_struct(p):
    """
        decl : new_type_dec
    """
    p[0] = p[1]

# ================ declarators ==================


def p_declarators(p):
    """
        declarators : declarator_1 ',' declarators
    """
    p[0] = n("declarators", [p[1]] + p[3].children)


def p_declarator_end(p):
    """
        declarators : declarator_1
    """
    p[0] = n("declarators", [p[1]])


def p_declarator_1(p):
    """
        declarator_1    : declarator_2
    """
    p[0] = p[1]


def p_declarator_1_winit(p):
    """
        declarator_1    : declarator_2 '=' initializer
    """
    p[0] = n("init", [p[1], p[3]])


def p_declarator_2_single(p):
    """
        declarator_2    : ID
    """
    p[0] = n("var", [], (p[1], ))


def p_declarator_2_func(p):
    """
        declarator_2    : ID '(' ')'
    """
    p[0] = n("func_decl", [], info=(p[1],))


def p_declarator_2_array(p):
    """
        declarator_2    : ID '[' ']'
    """
    p[0] = n("arr_decl", [], info=(p[1],))


def p_initializer(p):
    """
        initializer : NUMBER
                    | CHR
                    | STR
    """
    p[0] = n("const", [], (p[1],))

# ---------------- declarators end -----------------


# ================= new_type ======================


def p_new_type_dec(p):
    """
        new_type_dec    : new_type ID '{' new_type_params '}' ';'
    """
    p[0] = n(p[1], p[4], p[2])


def p_new_type(p):
    """
        new_type    : STRUCT
                    | CLASS
    """
    p[0] = p[1]


def p_new_type_params(p):
    """
        new_type_params : new_type_param new_type_params 
    """
    p[0] = [p[1]] + p[2]


def p_new_type_params_end(p):
    """
        new_type_params : new_type_param
    """
    p[0] = [p[1]]


def p_new_type_param(p):
    """
        new_type_param : type declarators ';'
    """
    p[0] = n("decl", [p[2]], (p[1],))


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
