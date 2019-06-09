'''
@author: xky
'''
from .Token import Token, TokenType
from .Keyword import KEYWORD_MAP
from .punc import SINGLE_PUNC_MAP

ESCAPE_CHAR_MAP = {
    'n': '\n',
    'r': '\r',
    't': '\t',
    'b': '\b',
    'f': '\f',
    '0': '\0'
}



class Lexer:
    def __init__(self, buffer: str):
        self.buffer = buffer
        self.column_number = 0
        self.line_number = 1
        self.tokens: [Token] = []
        self._char_index = 0
        self._buffer_len = len(buffer)

    def push_token(self, token_type, data=None):
        self.tokens.append(Token(token_type, self.column_number, self.line_number, data))

    def next(self) -> str:
        self._char_index += 1
        return self.buffer[self._char_index - 1]

    def preview_next(self) -> str:
        return self.buffer[self._char_index]

    def next_is(self, peek: str) -> bool:
        return self.preview_next() == peek

    def read_line(self) -> str:
        buf, *_ = self.buffer[self._char_index:].splitlines()
        self._char_index += len(buf)
        return buf

    def is_end(self):
        return self._char_index == self._buffer_len

    def lex(self) -> [Token]:
        while not self.is_end():
            self.column_number += 1
            char = self.next()
            if char == '"' or char == "'":
                buf = []
                str_len = len(buf)
                self.push_token(TokenType.StringLiteral, data="".join(buf))
                self.column_number += str_len + 1
            elif char.isdigit():
                buf = [char]
                while True:
                    ch = self.preview_next()
                    if ch == '.' or ch.isdigit():
                        self._char_index+=1
                        buf.append(ch)
                    else:
                        break
                self.push_token(TokenType.NumericLiteral, data=int(''.join(buf)))
            elif char == '/':
                next_char = self.preview_next()
                if next_char == '/':
                    self.next()
                    comment = self.read_line()
                    self.push_token((TokenType.Comment,), data=comment)
                    self.line_number += 1
                    self.column_number = 0
            elif char.isalpha() or char == '_':
                buf = [char]
                while True:
                    ch = self.preview_next()
                    if ch.isalpha() or ch.isdigit() or ch == '_':
                        buf.append(self.next())
                    else:
                        break
                buf = ''.join(buf)
                if KEYWORD_MAP.get(buf) is not None:
                    self.push_token(KEYWORD_MAP[buf],data=buf)
                elif buf == 'null':
                    self.push_token(TokenType.NullLiteral,data=buf)
                else:
                    self.push_token(TokenType.Identifier, data=buf)
                self.column_number += len(buf) - 1
            elif SINGLE_PUNC_MAP.get(char) is not None:
                self.push_token(SINGLE_PUNC_MAP[char],data=char)
            elif char == '/':
                next_char = self.preview_next()
                if next_char == '/':
                    self.next()
                    comment = self.read_line()
                    self.push_token(TokenType.Comment, data=comment)
                    self.line_number += 1
                    self.column_number = 0
                elif next_char == '*':
                    buf = []
                    self.next()
                    while True:
                        ch = self.next()
                        if ch == '*' and self.next_is('/'):
                            break
                        buf.append(ch)
                    self.push_token(TokenType.Comment, data=''.join(buf))
                    self.column_number += len(buf)
                elif next_char == '=':
                    self.next()
                    self.push_token(TokenType.AssignDiv,data='*=')
                    self.column_number += 1
                else:
                    self.push_token(TokenType.Div,data='/')
            elif char == '*':
                next_char = self.preview_next()
                if next_char == '=':
                    self.push_token(TokenType.AssignMul,data='*=')
                    self.next()
                    self.column_number += 1
                else:
                    self.push_token(TokenType.Mul,data='*')
            elif char == '+':
                next_char = self.preview_next()
                if next_char == '=':
                    self.push_token(TokenType.AssignMul,data='+=')
                    self.next()
                    self.column_number += 1
                elif next_char == '+':
                    self.push_token(TokenType.Inc,data='++')
                    self.next()
                    self.column_number += 1
                else:
                    self.push_token(TokenType.Add,data='+')
            elif char == '-':
                next_char = self.preview_next()
                if next_char == '=':
                    self.push_token(TokenType.AssignSub,data='-=')
                    self.next()
                    self.column_number += 1
                elif next_char == '-':
                    self.push_token(TokenType.Dec,data='--')
                    self.next()
                    self.column_number += 1
                else:
                    self.push_token(TokenType.Sub,data='-')
            elif char == '%':
                next_char = self.preview_next()
                self.push_token(TokenType.Mod)
            elif char == '=':
                next_char = self.preview_next()
                self.push_token(TokenType.Assign,data='=')
            elif char == '<':
                next_char = self.preview_next()
                self.push_token(TokenType.LessThan,data='<')
            elif char == '>':
                next_char = self.preview_next()
                self.push_token(TokenType.GreaterThan,data='>')
            # 判断换行
            elif char == '\n' or char == '\u2028' or char == '\u2029':
                self.line_number += 1
                self.column_number = 0
            elif char == '\r':
                self.column_number = 0
            elif char == ' ':
                pass
            else:
                print(f"{self.line_number}:{self.column_number}: error '{char}'")
        return self.tokens
