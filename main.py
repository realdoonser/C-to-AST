from lexer import *

if __name__ == "__main__":
    with open(sys.argv[-1]) as f:
        data = f.read()
    lexer = make_lexer()
    lexer.input(data)
    for tok in lexer:
        print(tok)
