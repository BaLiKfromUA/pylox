import typing

from pylox.error import LoxSyntaxError
from pylox.tokens import Token, TokenType


def is_alpha(char: str) -> bool:
    """Create a custom "is alphabetic" checker, as `str.isalpha` doesn't include underscores."""
    return any(
        (
            "a" <= char <= "z",
            "A" <= char <= "Z",
            char == "_",
        )
    )


def is_alnum(char: str) -> bool:
    """Create a custom "is alphanumeric" checker, as `str.alnum` doesn't include underscores."""
    return any(
        (
            is_alpha(char),
            char.isdigit(),
        )
    )


RESERVED = {
    "and": TokenType.AND,
    "class": TokenType.CLASS,
    "else": TokenType.ELSE,
    "false": TokenType.FALSE,
    "for": TokenType.FOR,
    "fun": TokenType.FUN,
    "if": TokenType.IF,
    "nil": TokenType.NIL,
    "or": TokenType.OR,
    "print": TokenType.PRINT,
    "return": TokenType.RETURN,
    "super": TokenType.SUPER,
    "this": TokenType.THIS,
    "true": TokenType.TRUE,
    "var": TokenType.VAR,
    "while": TokenType.WHILE,
}


class Scanner:
    def __init__(self, src: str) -> None:
        self.src = src
        self.tokens = list[Token]()
        self.line = 1
        self.start = 0
        self.current = 0

    def scan_tokens(self) -> list[Token]:
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def add_token(
            self, token_type: TokenType, literal: typing.Any = None
    ) -> None:
        text = self.src[self.start: self.current]
        self.tokens.append(Token(token_type, text, literal, self.line))

    def is_at_end(self) -> bool:
        return self.current >= len(self.src)

    def advance(self) -> str:
        token = self.src[self.current]
        self.current += 1
        return token

    def peek(self) -> str:
        if self.is_at_end():
            return "\0"
        return self.src[self.current]

    def peek_next(self) -> str:
        if self.current + 1 >= len(self.src):
            return "\0"
        return self.src[self.current + 1]

    def match(self, expected: str) -> bool:
        if self.is_at_end() or self.src[self.current] != expected:
            return False

        self.current += 1
        return True

    def scan_token(self) -> None:
        c = self.advance()
        match c:
            case "(":
                self.add_token(TokenType.LEFT_PAREN)
            case ")":
                self.add_token(TokenType.RIGHT_PAREN)
            case "{":
                self.add_token(TokenType.LEFT_BRACE)
            case "}":
                self.add_token(TokenType.RIGHT_BRACE)
            case ",":
                self.add_token(TokenType.COMMA)
            case ".":
                self.add_token(TokenType.DOT)
            case "-":
                self.add_token(TokenType.MINUS)
            case "+":
                self.add_token(TokenType.PLUS)
            case ";":
                self.add_token(TokenType.SEMICOLON)
            case "*":
                self.add_token(TokenType.STAR)
            case "!":
                self.add_token(
                    TokenType.BANG_EQUAL if self.match("=") else TokenType.BANG
                )
            case "=":
                self.add_token(
                    TokenType.EQUAL_EQUAL
                    if self.match("=")
                    else TokenType.EQUAL
                )
            case "<":
                self.add_token(
                    TokenType.LESS_EQUAL if self.match("=") else TokenType.LESS
                )
            case ">":
                self.add_token(
                    TokenType.GREATER_EQUAL
                    if self.match("=")
                    else TokenType.GREATER
                )
            case "/":
                if self.match("/"):
                    while self.peek() != "\n" and not self.is_at_end():
                        self.advance()
                else:
                    self.add_token(TokenType.SLASH)
            case " " | "\r" | "\t":
                # ignore whitespaces
                pass
            case "\n":
                self.line += 1
            case '"':
                self.string()
            case _:
                if c.isdigit():
                    self.number()
                elif is_alpha(c):
                    self.identifier()
                else:
                    raise LoxSyntaxError(
                        self.line, f"Unexpected character: '{c}'"
                    )

    def identifier(self):
        while is_alnum(self.peek()):
            self.advance()

        # If the lexeme does not match a reserved keyword, then it is considered an identifier
        lexeme = self.src[self.start: self.current]
        token_type = RESERVED.get(lexeme, TokenType.IDENTIFIER)

        self.add_token(token_type)

    def number(self):
        while self.peek().isdigit():
            self.advance()

        is_float = False
        if self.peek() == "." and self.peek_next().isdigit():
            is_float = True
            self.advance()  # consume dot
            while self.peek().isdigit():
                self.advance()

        literal = self.src[self.start: self.current]
        self.add_token(
            TokenType.NUMBER, float(literal) if is_float else int(literal)
        )

    def string(self):
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == "\n":
                self.line += 1
            self.advance()

        if self.is_at_end():
            raise LoxSyntaxError(self.line, "Unterminated string.")

        # The closing ".
        self.advance()

        # Trim the surrounding quotes.
        value = self.src[self.start + 1: self.current - 1]
        self.add_token(TokenType.STRING, value)
