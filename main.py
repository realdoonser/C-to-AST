from lexer import *

data = """
void main(){
    int a = 3 ;
    return 1;
}
"""

lexer.input(data)

token_stream = []

if __name__ == "__main__":
    for tok in lexer:
        token_stream.append(tok)
    print(token_stream[0])