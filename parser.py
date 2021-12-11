import ply.yacc as yacc
from lexer import tokens
import sys
import pprint


precedence = (
    ('left', '?', ':'),
    ('left', 'LOGOR'),
    ('left', 'LOGAND'),
    ('left', '^'),
    ('left', 'LOGEQ', 'LOGNEQ'),
    ('left', '<', '>', 'LEQ', 'GEQ'),
    ('left', 'LSHIFT', 'RSHIFT'),
    ('left', '+', '-'),
    ('left', '*', '/'),
    ('right', 'LPLUSPLUS', 'LMINUSMINUS', 'LPOS', 'LNEG', 'LNOT'),
    ('left', 'RPLUSPLUS', 'RMINUSMINUS', '.', 'RARROW')
)


class n:
    def __init__(self, type, children=[], info=None) -> None:
        self.type = type
        self.children = children
        self.info = info

    def __repr__(self) -> str:
        return pprint.pformat({"type": self.type, "info": self.info, "children": self.children}, width=500, sort_dicts=False)


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
        external_decl   : decl ';'
                        | func_def
    """
    p[0] = n("external_decl", [p[1]])


def p_decl(p):
    """
        decl    : usual_dec
                | new_type_dec
    """
    p[0] = p[1]


def p_usual_decl(p):
    """
        usual_dec : type declarators
    """
    p[0] = n("usual_decl", [p[2]], p[1])

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
    p[0] = n("var", [], p[1])


def p_declarator_2_func(p):
    """
        declarator_2    : ID '(' ')'
    """
    p[0] = n("func_decl", [], info=p[1])


def p_declarator_2_array(p):
    """
        declarator_2    : ID '[' ']'
    """
    p[0] = n("arr_decl", [], info=p[1])


def p_declarator_2_arrray(p):
    """
        declarator_2    : ID '[' expression ']'
    """
    p[0] = n("arr_decl", [p[3]], info=p[1])


def p_initializer(p):
    """
        initializer : expression
                    | '{' expressions '}'
    """
    if (len(p) == 2):
        p[0] = n("initializer", [p[1]])
    else:
        p[0] = n("initializer", [p[2]])


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
    p[0] = n("param", [p[2]], p[1])

# ------------------ new types end -------------------


def p_function_definition(p):
    """
        func_def : type ID '(' params ')' '{' statements '}'
    """
    p[0] = n("func_def", [p[7]], (p[1], p[2], p[3]))


def p_function_defintion_noparam(p):
    """
        func_def : type ID '(' ')' '{' statements '}'
    """
    p[0] = n("func_def", [p[6]], (p[1], p[2]))


def p_function_defintion_nostatement(p):
    """
        func_def : type ID '(' params ')' '{' '}'
    """
    p[0] = n("func_def", [], (p[1], p[2], p[4]))


def p_function_definition_nothing(p):
    """
        func_def : type ID '(' ')' '{' '}'
    """
    p[0] = n("func_def", [], (p[1], p[2]))


def p_params(p):
    """
        params : param ',' params
    """
    p[0] = n("params", p[1] + p[3].children)


def p_params_end(p):
    """
        params : param
    """
    p[0] = n("params", [p[1]])


def p_param(p):
    """
        param : type declarator_2
    """
    p[0] = n("param", [p[2]], p[1])

# =================== statement start ======================


def p_statements(p):
    """
        statements : statement statements
    """
    if (p[1] != None):
        p[0] = n("statements", [p[1]] + p[2].children)
    else:
        p[0] = n("statements", p[2].children)


def p_statements_end(p):
    """
        statements : statement
    """
    p[0] = n("statements", [p[1]])


def p_statement(p):
    """
        statement   : expression ';'
                    | decl ';'
                    | conditional
                    | iteration
                    | jump ';'
    """
    p[0] = p[1]


def p_statement_extra_semicolon(p):
    """
        statement : ';'
    """
    pass

# ================== conditional statement ==================


def p_conditional(p):
    """
        conditional : IF '(' expression ')' '{' stats_or_null '}'
    """
    p[0] = n("conditional", [p[3], p[6]])


def p_conditional_elseif(p):
    """
        conditional : IF '(' expression ')' '{' stats_or_null '}' ELSE conditional
    """
    p[0] = n("conditional", [p[3], p[6]], "else")


def p_conditional_else(p):
    """
        conditional : IF '(' expression ')' '{' stats_or_null '}' ELSE '{' stats_or_null '}'
    """
    p[0] = n("conditional", [p[3], p[10]], "else")

# -------------------- conditional end -------------------


def p_block(p):
    """
        statement : '{' stats_or_null '}'
    """
    p[0] = n("block", p[2])


def p_statement_or_null(p):
    """
        stats_or_null   : statements
                        | empty
    """
    if (len(p) == 2):
        p[0] = p[1]

# ===================== iteration =========================


def p_iteration(p):
    """
        iteration : WHILE '(' expression ')' '{' stats_or_null '}'
    """
    p[0] = n(p[1], [p[3], p[6]])


def p_iteration_do_while(p):
    """
        iteration : DO '{' stats_or_null '}' WHILE '(' expression ')' ';'
    """
    p[0] = n("dowhile", [p[3], p[7]])


def p_iteration_for(p):
    """
        iteration : FOR '(' expr_or_null_or_init ';' expr_or_null ';' expr_or_null ')' '{' stats_or_null '}'
    """
    p[0] = n("for", [p[3], p[5], p[7], p[10]])


def p_expr_or_null(p):
    """
        expr_or_null    : expression
                        | empty
    """
    p[0] = p[1]


def p_expr_or_null_or_init(p):
    """
        expr_or_null_or_init    : expr_or_null
                                | usual_dec
    """
    p[0] = p[1]


def p_assignment_expr(p):
    """
        assignment_expr : ID assignmenteq_op expression
    """
    var = n("var", [], p[1])
    p[0] = n("assignemnteq_expr", [var, p[3]], p[2])


def p_assignment_op(p):
    """
        assignmenteq_op     : '='
                            | MULTEQ
                            | ADDEQ
                            | SUBEQ
                            | MODEQ
                            | DIVEQ
    """
    p[0] = p[1]


def p_jump(p):
    """
        jump    : BREAK
                | CONTINUE
                | RETURN
    """
    p[0] = n(p[1])


def p_jump_wvalue(p):
    """
        jump : RETURN expression
    """
    p[0] = n(p[1], [p[2]])

# -------------------- statement end ------------------------


# ===================== expression =========================

def p_expressions(p):
    """
        expressions : expression ',' expressions
    """
    p[0] = n("expressions", [p[1]] + p[3].children)


def p_expressions_end(p):
    """
        expressions : expression
    """
    p[0] = n("expressions", [p[1]])


def p_expression(p):
    """
        expression  : bin_expr
                    | assignment_expr
    """
    p[0] = p[1]


def p_expression_wternary(p):
    """
        expression  : bin_expr '?' bin_expr ':' bin_expr
    """
    p[0] = n("expr_ternary", [p[1], p[3], p[5]])


def p_binary_expr(p):
    """
        bin_expr    : pre_unary_expr bin_op bin_expr
    """
    p[0] = n("binary_expression", [p[1], p[3]], p[2])


def p_binary_to_unary(p):
    """
        bin_expr    : pre_unary_expr
    """
    p[0] = p[1]


def p_binary_operator(p):
    """
        bin_op      : '+'
                    | '-'
                    | '*'
                    | '/'
                    | LOGAND
                    | LOGOR
                    | LOGEQ
                    | LOGNEQ
                    | LSHIFT
                    | RSHIFT
                    | '<'
                    | '>'
                    | LEQ
                    | GEQ
                    | '^'	
    """
    p[0] = p[1]


def p_pre_unary_expr(p):
    """
        pre_unary_expr  : PLUSPLUS pre_unary_expr %prec LPLUSPLUS
                        | MINUSMINUS pre_unary_expr %prec LMINUSMINUS
                        | '+' pre_unary_expr %prec LPOS
                        | '-' pre_unary_expr %prec LNEG
                        | '!' pre_unary_expr %prec LNOT
    """
    p[0] = n("pre_unary", [p[2]], p[1])


def p_pre_unary_to_post(p):
    """
        pre_unary_expr : post_unary_expr
    """
    p[0] = p[1]


def p_post_unary_expr_array(p):
    """
        post_unary_expr : post_unary_expr '[' expression ']'
    """
    p[0] = n("post_unary", [p[1], p[3]], "array_access")


def p_post_unary_fncall_empty(p):
    """
        post_unary_expr : post_unary_expr '(' ')'
    """
    p[0] = n("post_unary", [p[1]], "fncall")


def p_post_unary_fncall(p):
    """
        post_unary_expr : post_unary_expr '(' expressions ')'
    """
    p[0] = n("post_unary", [p[1], p[3]], "fncall")


def p_post_unary_ppmm(p):
    """
        post_unary_expr : post_unary_expr PLUSPLUS %prec RPLUSPLUS
                        | post_unary_expr MINUSMINUS %prec RMINUSMINUS
    """
    p[0] = n("post_unary", [p[1]], p[2])


def p_post_unary_access_member(p):
    """
        post_unary_expr : post_unary_expr '.' ID
                        | post_unary_expr RARROW ID
    """
    p[0] = n("post_unary", [p[1], p[3]], p[2])


def p_post_unary_to_element(p):
    """
        post_unary_expr : element
    """
    p[0] = p[1]


def p_element(p):
    """
        element : ID
    """
    p[0] = n("var", [], p[1])


def p_element_const(p):
    """
        element : NUMBER
                | CHR
                | STR
    """
    p[0] = n("const", [], p[1])

# ------------------- expression end -----------------------


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
    p[0] = p[1]


def p_empty(p):
    """
        empty :
    """
    pass


parser = yacc.yacc()

if __name__ == "__main__":
    with open(sys.argv[-1]) as f:
        data = f.read()
    result: n = parser.parse(data)
    print(result)
