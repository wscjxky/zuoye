class Punctuator:
    OpenBlock = 33, "{"
    CloseBlock = 34, "}"
    OpenParen = 35, "("
    CloseParen = 36, ")"
    OpenBracket = 37, "["
    CloseBracket = 38, "]"
    Dot = 39, "."
    Semicolon = 40, ";"
    Comma = 41, ","
    LessThan = 42, "<"
    GreaterThan = 43, ">"
    Add = 48, "+"
    Sub = 49, "-"
    Mul = 50, "*"
    Div = 51, "/"
    Mod = 52, "%"
    Inc = 53, "++"
    Dec = 54, "--"
    LeftSh = 55, "<<"
    RightSh = 56, ">>"
    Colon = 65, ":"
    Assign = 66, "="
    AssignAdd = 67, "+="
    AssignSub = 68, "-="
    AssignMul = 69, "*="
    AssignDiv = 70, "/="

SINGLE_PUNC_MAP = {
    ';': Punctuator.Semicolon,
    ':': Punctuator.Colon,
    '.': Punctuator.Dot,
    '(': Punctuator.OpenParen,
    ')': Punctuator.CloseParen,
    ',': Punctuator.Comma,
    '{': Punctuator.OpenBlock,
    '}': Punctuator.CloseBlock,
    '+': Punctuator.Add,
    '-': Punctuator.Sub,
    '*': Punctuator.Mul,
    '%': Punctuator.Mod,
    '=': Punctuator.Assign,
    '+=': Punctuator.AssignAdd,
    '-=': Punctuator.AssignSub,
    '*=': Punctuator.AssignMul,
    '/=': Punctuator.AssignDiv,

}
