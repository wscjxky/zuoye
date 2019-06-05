'''
@author: xky
'''
from .Keyword import Keyword
from .punc import Punctuator
from .pos import Position


class TokenType(Keyword, Punctuator):
    EOF = 78,
    Identifier = 79,
    NullLiteral = 80, "null"
    NumericLiteral = 81,
    StringLiteral = 82,
    Comment = 83


class Token:
    def __init__(self, token_type, col_num, line_num, data=None):
        self.token_type = token_type
        self.pos = Position(col_num, line_num)
        self.data = data

    def __str__(self):
        return f"{self.token_type[0]}, {self.data if self.data is not None else ''}"

    def __repr__(self):
        return f"({str(self)})"
