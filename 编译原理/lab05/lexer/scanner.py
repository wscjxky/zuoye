'''
@author: xky
'''
from .lexer import *
from .Token import Token, TokenType
from .Keyword import KEYWORD_MAP
from .punc import SINGLE_PUNC_MAP
from config import *


def gen_tokens():
    with open(input_c_file, encoding='utf8') as c_file:
        lexer = Lexer(c_file.read())
        with open(token_file, mode='w', encoding='utf8') as tokens_file:
            for token in lexer.lex():
                tokens_file.write(str(token) + '\n')
 # 清洗数据转换为想要的表达式
def gen_input_str():
    input_str1 = ''
    source_str=''
    with open(token_file, mode='r', encoding='utf8') as tokens_file:
        for line in tokens_file.readlines():
            line = line.strip('\n')
            token = int(line.split(', ')[0])
            word = line.split(', ')[1]
            # 跳过注释和分号
            if word == ';' or token == TokenType.Comment:
                continue
            elif word in KEYWORD_MAP.keys():
                if word == 'if':
                    input_str1 += 'i'
                elif word == 'return':
                    input_str1 += 'r'
                else:
                    input_str1 += 'k'
            elif token == TokenType.Identifier[0]:
                if word == 'main':
                    input_str1 += 'm'
                else:
                    input_str1 += 'v'
            elif word in SINGLE_PUNC_MAP.keys():
                input_str1 += word
            elif token == TokenType.NumericLiteral[0]:
                input_str1 += 'd'
            source_str+=' '+word
        source_str=source_str.strip()
        print(source_str.split(' '))
        input_str1 += '#'
    with open(input_str_file, mode='w', encoding='utf8') as f:
        f.write(input_str1)
    with open(input_source_file, mode='w', encoding='utf8') as f:
        f.write(source_str)

