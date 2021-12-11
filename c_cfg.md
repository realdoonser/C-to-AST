# Subset C's CFG (BNF)

Syntax rules for subset of C we are working with.

```c
program : include program
        | external_decl program
        | include
        | external_decl

include : # ID < ID . ID >

/* External Declarations (函数外声明) */
exernal_decl    : decl // int a = 10; etc.
                | func_def // void f(){ ... }

/* decl */

decl    : type declarators ; // int a, b=2, d, g();
        | new_type_dec // new class or struct

type    : VOID | CHAR | SHORT | INT | LONG | FLOAT | DOUBLE

/* struct class begin: */
// self defined data structures (struct, class)

new_type_dec    : new_type ID { new_type_params } ;
                | new_type ID { new_type_params } new_type_inits ;

new_type : CLASS | STRUCT

// only support the simple params
new_type_params : new_type_param; new_type_params
                | new_type_param; // inside struct {... int a; ...} where int a; is the param

new_type_param  : type ID ;

new_type_inits  : ID , new_type_inits
                | ID

/* struct class end */

// can can many declarator (eg. int a,b,c,d,e )
declarators : declarator_1
            | declarator_1 , declarators

// level 1 of declaration, assign or not
declarator_1    : declarator_2 = initializer // pointers
                | declarator_2

// level 2 of declaration, pointer or not
declarator_2    : * declarator_3
                | declarator_3

// level 3 of declaration, parenthasis/function declaration etc. may have to go up a level: eg. char (*(*x())[])() function returning pointer to array[] of pointer to function returning char
declaration_3   : ID
                | ( declarator_2 )
                | declarator_2 [ expression ]
                | declarator_2 [  ]
                | declarator_2 ( params )
                | declarator_2 (  )

// params eg. int a, int, float * etc.
params  : param , params
        | param

param   : type declarator_2

// initializer used in declarator_1

initializer : expression
            | { expressions }

expressions : expression , expressions
            | expression

/* function definition */

func_def        : type ID ( params ) { statements }
                | type ID ( ) { statements }
                | VOID ID ( params ) { }
                | VOID ID (  ) { }

// c statements

statements  : statement statements
            | statement

statement       : expression ; // a+1*10
                | decl ; // int a = 10;
                | { statements } // block statements
                | conditional // if () {} else {}
                | iteration // while () {}
                | jump
                | ; // many ;'s

assignment_expr : ID assignment_op expression

assignment_op   : = | *= | /= | %= | += | -= | <<=
                | >>= | $= | ^= | |=

conditional     : if ( expression ) { stats_or_null }
                | if ( expression ) else conditional // higher precedence
                | if ( expression ) { stats_or_null } else { stats_or_null } // lower precedence

iteration       : while ( expression ) { stats_or_null }
                | do { stats_or_null } while ( expression ) ;
                | for ( expr_or_null_or_init ; expr_or_null ; expr_or_null ) { stats_or_null }

stats_or_null : statements // statements or empty
                | empty

expr_or_null    : expression
                | empty

expr_or_null_or_init    : expr_or_null
                        | declarator_1

jump            : break ;
                | continue ;
                | return ;
                | return expression ;

/* expressions in the order of operation */
expression      : or_expr ? or_expr : or_expr
                | or_expr
                | assignment_expr

or_expr         : and_expr || and_expr
                | and_expr

and_expr        : xor_expr && xor_expr
                | xor_expr

xor_expr        : eq_expr ^ eq_expr
                | eq_expr

eq_expr         : rel_expr
                | eq_expr == rel_expr
                | eq_expr != rel_expr

rel_expr        : shift_expr
                | rel_expr < shift_expr
                | rel_expr > shift_expr
                | rel_expr <= shift_expr
                | rel_expr >= shift_expr

shift_expr      : add_expr
                | shift_expr << add_expr
                | shift_expr >> add_expr

add_expr        : mult_expr
                | add_expr + mult_expr
                | add_expr - mult_expr

mult_expr       : unary_expr
                | mult_expr * unary_expr
                | mult_expr / unary_expr

unary_expr      : post_unary_expr
                | ++ unary_expr
                | -- unary_expr
                | + uanry_expr
                | - uanry_expr
                | ! unary_expr

post_unary_expr : element
                | post_unary_expr [ expr ]
                | post_unary_expr ( expressions_comma )
                | post_unary_expr ( )
                | post_unary_expr ++
                | post_uanry_expr --
                | post_unary_expr . ID
                | post_unary_expr -> ID

expressions_comma       : expression , expression_comma
                        | expression

element : ID
        | NUMBER

```

Currently not supprted styles (that i know of):

```c
#define
typedef
class ;// with public private
int * bar(); // functions that return complex types
struct ... {... } *i_1, i_2[10], *i_3[20]; // struct with complex initializations (eg. *i_1 )
int foo(int, float, int) // function definition with type but no var name
int foo(float a, ...) // stdarg style three dots ...
if (a = b)
    do stuff // if/for/while statements without {}
a | b // bitwise operations
switch () // switch statements
goto // will not plan on adding
```
