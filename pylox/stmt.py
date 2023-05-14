# THIS CODE IS GENERATED AUTOMATICALLY. DO NOT CHANGE IT MANUALLY!

import typing
from abc import ABC, abstractmethod

from pylox.expr import Expr


class StmtVisitor(ABC):
    @abstractmethod
    def visit_expression_stmt(self, stmt) -> typing.Any:
        pass

    @abstractmethod
    def visit_print_stmt(self, stmt) -> typing.Any:
        pass


class Stmt:
    def __init__(self):
        pass

    @abstractmethod
    def accept(self, visitor: StmtVisitor) -> typing.Any:
        pass


class Expression(Stmt):
    def __init__(self, expr: Expr):
        super().__init__()
        self.expr = expr

    def accept(self, visitor: StmtVisitor) -> typing.Any:
        return visitor.visit_expression_stmt(self)


class Print(Stmt):
    def __init__(self, expr: Expr):
        super().__init__()
        self.expr = expr

    def accept(self, visitor: StmtVisitor) -> typing.Any:
        return visitor.visit_print_stmt(self)
