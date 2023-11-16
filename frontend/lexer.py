from enum import auto, Enum


class TokenType(Enum):
    NUMBER = "N",
    IDENTIFIER = "I",
    EQUALS = "E",
    COMMA = "COM",
    COLON = "COL",
    OPENPAREN = "O",
    CLOSEPAREN = "C",
    OPENBRACE = "OB",
    CLOSEBRACE = "CB",
    OPENBRACKET = "OR",
    CLOSEBRACKET = "CR",
    BINARYOP = "B",
    LET = "L",
    CONST = "CONST",
    USER = "U",
    EOF = "EOF",
    STRING = "STR",
    SEMI = "SEMICOLON",
    DOT = ".",
    FN = "FN",
    NEWLINE = "NL",


Keywords = {
    'o' : TokenType.LET,
    'anteAla' : TokenType.CONST,
    'ilo': TokenType.FN,
    'li': TokenType.EQUALS,
}

class Token:
    def __init__(self, value: str, type: TokenType):
        self.value = value
        self.type = type

def isSkippable (src: str):
    return src == ' ' or src == '\t' or src[0] == '\n' or src[0] == "\r"

def tokenize(srcCode):
    tokens = []
    src = [*srcCode]

    while len(src) > 0:
        if src[0] == '(':
            tokens.append(Token(src.pop(0), TokenType.OPENPAREN))
        elif src[0] == ')':
            tokens.append(Token(src.pop(0), TokenType.CLOSEPAREN))
        elif src[0] == '{':
            tokens.append(Token(src.pop(0), TokenType.OPENBRACE))
        elif src[0] == '}':
            tokens.append(Token(src.pop(0), TokenType.CLOSEBRACE))
        elif src[0] == '[':
            tokens.append(Token(src.pop(0), TokenType.OPENBRACKET))
        elif src[0] == ']':
            tokens.append(Token(src.pop(0), TokenType.CLOSEBRACKET))
        ##elif src[0] == '\n' or src[0] == "\r":
            #tokens.append(Token(src.pop(0), TokenType.NEWLINE))
        elif src[0] == '+' or src[0] == '-' or src[0] == '*' or src[0] == '/' or src[0] == '%':
            tokens.append(Token(src.pop(0), TokenType.BINARYOP))
        elif src[0] == '=':
            tokens.append(Token(src.pop(0), TokenType.EQUALS))
        elif src[0] == ';':
            tokens.append(Token(src.pop(0), TokenType.SEMI))
        elif src[0] == ':':
            tokens.append(Token(src.pop(0), TokenType.COLON))
        elif src[0] == ',':
            tokens.append(Token(src.pop(0), TokenType.COMMA))
        elif src[0] == '.':
            tokens.append(Token(src.pop(0), TokenType.DOT))
        else:
            if src[0].isnumeric():
                num = ""
                while len(src) > 0 and src[0].isnumeric():
                    num = num + src.pop(0)
                tokens.append(Token(num, TokenType.NUMBER))
            elif src[0].isalpha():
                ident = ""
                while len(src) > 0 and src[0].isalpha():
                    ident += src.pop(0)
                if ident in Keywords:
                    tokens.append(Token(ident, Keywords[ident]))
                else:
                    tokens.append(Token(ident, TokenType.IDENTIFIER))
            elif isSkippable(src[0]):
                src.pop(0)
            else:
                raise ValueError("Unrecognized char: " + src[0])
    tokens.append(Token(None, TokenType.EOF))
    print("Tokens:")
    for i in tokens:
        print("value: ", str(i.value), " type: ", str(i.type))
    return tokens
        
    