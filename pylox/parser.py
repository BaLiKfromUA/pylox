from typing import List

import pylox.expr as ast
from pylox.error import LoxParseError
from pylox.scanner import Token, TokenType


# recursive descent, top-down parser
class Parser:
    def __init__(self, tokens: List[Token]) -> None:
        self.tokens = tokens
        self.current = 0

    def parse(self) -> ast.Expr:
        return self.expression()

    # helpers
    def match(self, *token_types: TokenType) -> bool:
        for token_type in token_types:
            if self.check(token_type):
                self.advance()
                return True
        return False

    def check(self, token_type: TokenType) -> bool:
        if self.is_at_end():
            return False
        return self.peek().token_type == token_type

    def advance(self) -> Token:
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def is_at_end(self) -> bool:
        return self.peek().token_type == TokenType.EOF

    def peek(self) -> Token:
        return self.tokens[self.current]

    def previous(self) -> Token:
        return self.tokens[self.current - 1]

    # error handling
    def consume(self, expected: TokenType, msg: str) -> Token:
        if self.check(expected):
            return self.advance()

        raise LoxParseError(self.peek(), msg)

    def synchronize(self) -> None:
        self.advance()
        while not self.is_at_end():
            if self.previous().token_type == TokenType.SEMICOLON:
                return
            if self.peek().token_type == TokenType.CLASS:
                return
            elif self.peek().token_type == TokenType.FUN:
                return
            elif self.peek().token_type == TokenType.VAR:
                return
            elif self.peek().token_type == TokenType.FOR:
                return
            elif self.peek().token_type == TokenType.IF:
                return
            elif self.peek().token_type == TokenType.WHILE:
                return
            elif self.peek().token_type == TokenType.PRINT:
                return
            elif self.peek().token_type == TokenType.RETURN:
                return
            self.advance()

    # expressions
    def expression(self) -> ast.Expr:
        return self.equality()

    # equality       → comparison ( ( "!=" | "==" ) comparison )* ;
    def equality(self) -> ast.Expr:
        expr = self.comparison()

        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            op = self.previous()
            right = self.comparison()
            expr = ast.Binary(expr, op, right)

        return expr

    # comparison     → term ( ( ">" | ">=" | "<" | "<=" ) term )* ;
    def comparison(self) -> ast.Expr:
        expr = self.term()

        while self.match(
            TokenType.GREATER,
            TokenType.GREATER_EQUAL,
            TokenType.LESS,
            TokenType.LESS_EQUAL,
        ):
            op = self.previous()
            right = self.term()
            expr = ast.Binary(expr, op, right)

        return expr

    # term           → factor ( ( "-" | "+" ) factor )* ;
    def term(self) -> ast.Expr:
        expr = self.factor()

        while self.match(TokenType.MINUS, TokenType.PLUS):
            op = self.previous()
            right = self.factor()
            expr = ast.Binary(expr, op, right)

        return expr

    # factor         → unary ( ( "/" | "*" ) unary )* ;
    def factor(self) -> ast.Expr:
        expr = self.unary()

        while self.match(TokenType.SLASH, TokenType.STAR):
            op = self.previous()
            right = self.unary()
            expr = ast.Binary(expr, op, right)

        return expr

    # unary          → ( "!" | "-" ) unary | primary ;
    def unary(self) -> ast.Expr:
        if self.match(TokenType.BANG, TokenType.MINUS):
            op = self.previous()
            right = self.unary()
            return ast.Unary(op, right)

        return self.primary()

    # primary        → NUMBER | STRING | "true" | "false" | "nil" | "(" expression ")" ;
    def primary(self) -> ast.Expr:
        if self.match(TokenType.FALSE):
            return ast.Literal(False)
        if self.match(TokenType.TRUE):
            return ast.Literal(True)
        if self.match(TokenType.NIL):
            return ast.Literal(None)

        if self.match(TokenType.NUMBER, TokenType.STRING):
            return ast.Literal(self.previous().literal)

        if self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return ast.Grouping(expr)

        raise LoxParseError(self.peek(), "Expect expression")
