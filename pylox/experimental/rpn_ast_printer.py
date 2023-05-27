import typing

import pylox.expr as ast


# Define a visitor class for our syntax tree classes that takes an expression,
# converts it to RPN, and returns the resulting string.
class RpnAstPrinter(ast.ExprVisitor):
    def print_expr(self, expr: ast.Expr):
        return expr.accept(self)

    def visit_logical_expr(self, expr) -> typing.Any:
        raise NotImplementedError

    def visit_assign_expr(self, expr) -> typing.Any:
        raise NotImplementedError

    def visit_variable_expr(self, expr) -> typing.Any:
        raise NotImplementedError

    def visit_binary_expr(self, expr: ast.Binary):
        return f"{str(expr.left.accept(self))} {str(expr.right.accept(self))} {expr.operator.lexeme}"

    def visit_grouping_expr(self, expr: ast.Grouping):
        return expr.expr.accept(self)

    def visit_literal_expr(self, expr: ast.Literal):
        return str(expr.value)

    def visit_unary_expr(self, expr: ast.Unary):
        op = expr.operator.lexeme
        if op == "-":
            # Can't use same symbol for unary and binary.
            op = "~"
        return f"{str(expr.right.accept(self))} {op}"
