'''
@author: xky
'''
from .lexer import *
from .Token import Token, TokenType
from .Keyword import KEYWORD_MAP
from .punc import SINGLE_PUNC_MAP
from config import *


def gen_tokens(input_c_file=''):
    tokens_txt=''
    # 清洗数据转换为想要的表达式
    with open(input_c_file, encoding='utf8') as c_file:
        lexer = Lexer(c_file.read())
        with open(token_file, mode='w', encoding='utf8') as tokens_file:
            for token in lexer.lex():
                tokens_file.write(str(token) + '\n')
                tokens_txt+=(str(token) + '\n')
    return tokens_txt

def gen_input_str():
    input_str1 = ''
    source_str = ''
    with open(token_file, mode='r', encoding='utf8') as tokens_file:
        for line in tokens_file.readlines():
            line = line.strip('\n')
            token = int(line.split(', ')[0])
            word = line.split(', ')[1]
            # 跳过注释和分号
            if word == ';' or token == TokenType.Comment:
                continue
            elif word in KEYWORD_MAP.keys():
                # 关键字KEYWORD_MAP，if，return，int
                if word == 'if':
                    input_str1 += 'i'
                elif word == 'return':
                    input_str1 += 'r'
                else:
                    input_str1 += 'k'
            # 变量名 Identifier
            elif token == TokenType.Identifier[0]:
                if word == 'main':
                    input_str1 += 'm'
                else:
                    input_str1 += 'v'
            # 变量名 符号栈
            elif word in SINGLE_PUNC_MAP.keys():
                input_str1 += word
            elif token == TokenType.NumericLiteral[0]:
                input_str1 += 'd'
            source_str += ' ' + word
        source_str = source_str.strip()
        input_str1 += '#'
    # , 如果是cmp,<,>符号就变为c。
    # input_str1=input_str1.replace('<','c')
    print(source_str)
    print(input_str1)
    with open(input_str_file, mode='w', encoding='utf8') as f:
        f.write(input_str1)
    with open(input_source_file, mode='w', encoding='utf8') as f:
        f.write(source_str)
