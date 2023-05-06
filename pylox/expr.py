# THIS CODE IS GENERATED AUTOMATICALLY. DO NOT CHANGE IT MANUALLY!

import typing
from abc import ABC, abstractmethod

from pylox.tokens import Token


class ExprVisitor(ABC):
    @abstractmethod
    def visit_binary_expr(self, expr):
        pass

    @abstractmethod
    def visit_grouping_expr(self, expr):
        pass

    @abstractmethod
    def visit_literal_expr(self, expr):
        pass

    @abstractmethod
    def visit_unary_expr(self, expr):
        pass


class Expr:
    def __init__(self):
        pass

    @abstractmethod
    def accept(self, visitor: ExprVisitor):
        pass


class Binary(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr):
        super().__init__()
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor: ExprVisitor):
        return visitor.visit_binary_expr(self)


class Grouping(Expr):
    def __init__(self, expr: Expr):
        super().__init__()
        self.expr = expr

    def accept(self, visitor: ExprVisitor):
        return visitor.visit_grouping_expr(self)


class Literal(Expr):
    def __init__(self, value: typing.Any):
        super().__init__()
        self.value = value

    def accept(self, visitor: ExprVisitor):
        return visitor.visit_literal_expr(self)


class Unary(Expr):
    def __init__(self, operator: Token, right: Expr):
        super().__init__()
        self.operator = operator
        self.right = right

    def accept(self, visitor: ExprVisitor):
        return visitor.visit_unary_expr(self)
