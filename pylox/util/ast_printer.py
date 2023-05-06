import pylox.expr as ast


# utility class to test basics of AST
class AstPrinter(ast.ExprVisitor):

    def print_expr(self, expr: ast.Expr):
        return expr.accept(self)

    def visit_binary_expr(self, expr: ast.Binary):
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visit_grouping_expr(self, expr: ast.Grouping):
        return self.parenthesize("group", expr.expr)

    def visit_literal_expr(self, expr: ast.Literal):
        return str(expr.value)

    def visit_unary_expr(self, expr: ast.Unary):
        return self.parenthesize(expr.operator.lexeme, expr.right)

    def parenthesize(self, name, *expressions):
        out = "(" + name

        for expr in expressions:
            out += " "
            out += expr.accept(self)

        out += ")"
        return out
