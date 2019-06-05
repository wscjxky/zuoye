from lexer import *

if __name__ == '__main__':
    with open("test.c") as c_file:
        lexer = Lexer(c_file.read())
        with open("tokens.txt", mode='w') as tokens_file:
            for token in lexer.lex():
                tokens_file.write(str(token) + '\n')
