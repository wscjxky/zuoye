'''
@author: xky
'''
class Keyword:
    Int = 1, "int"
    Long = 2, "long"
    Short = 3, "short"
    Float = 4, "float"
    Double = 5, "double"
    Char = 6, "char"
    Unsigned = 7, "unsigned"
    Signed = 8, "signed"
    Const = 9, "const"
    Void = 10, "void"
    Volatile = 11, "volatile"
    Enum = 12, "enum"
    Struct = 13, "struct"
    Union = 14, "union"
    If = 15, "if"
    Else = 16, "else"
    Goto = 17, "goto"
    Switch = 18, "switch"
    Case = 19, "case"
    Do = 20, "do"
    While = 21, "while"
    For = 22, "for"
    Continue = 23, "continue"
    Break = 24, "break"
    Return = 25, "return"
    Default = 26, "default"
    Typeof = 27, "typeof"
    Auto = 28, "auto"
    Register = 29, "register"
    Extern = 30, "extern"
    Static = 31, "static"
    Sizeof = 32, "sizeof"


KEYWORD_MAP = {}

for key, val in Keyword.__dict__.items():
    if not key.startswith('__'):
        KEYWORD_MAP[val[1]] = val
