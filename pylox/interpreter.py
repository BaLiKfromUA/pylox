import typing

import pylox.expr as expr_ast
import pylox.stmt as stmt_ast
from pylox.error import LoxRuntimeError
from pylox.expr import Expr, ExprVisitor
from pylox.scanner import Token, TokenType
from pylox.stmt import Stmt, StmtVisitor


class Interpreter(ExprVisitor, StmtVisitor):
    def interpret(self, statements: list[Stmt]):
        for statement in statements:
            self.execute(statement)

    def execute(self, stmt: Stmt):
        stmt.accept(self)

    def evaluate(self, expr: Expr) -> typing.Any:
        return expr.accept(self)

    def visit_expression_stmt(self, stmt: stmt_ast.Expression) -> typing.Any:
        self.evaluate(stmt.expr)
        return None

    def visit_print_stmt(self, stmt: stmt_ast.Print) -> typing.Any:
        value = self.evaluate(stmt.expr)
        print(self.stringify(value))
        return None

    def visit_binary_expr(self, expr: expr_ast.Binary) -> typing.Any:
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        match expr.operator.token_type:
            case TokenType.GREATER:
                self.check_number_operands(expr.operator, left, right)
                return float(left) > float(right)
            case TokenType.GREATER_EQUAL:
                self.check_number_operands(expr.operator, left, right)
                return float(left) >= float(right)
            case TokenType.LESS:
                self.check_number_operands(expr.operator, left, right)
                return float(left) < float(right)
            case TokenType.LESS_EQUAL:
                self.check_number_operands(expr.operator, left, right)
                return float(left) <= float(right)
            case TokenType.MINUS:
                self.check_number_operands(expr.operator, left, right)
                return float(left) - float(right)
            case TokenType.BANG_EQUAL:
                return left != right
            case TokenType.EQUAL_EQUAL:
                return left == right
            case TokenType.PLUS:
                if self.is_number(left) and self.is_number(right):
                    return float(left) + float(right)

                if type(left) is str or type(right) is str:
                    return self.stringify(left) + self.stringify(right)

                raise LoxRuntimeError(
                    expr.operator,
                    "Operands must be two numbers or two strings.",
                )
            case TokenType.SLASH:
                self.check_number_operands(expr.operator, left, right)
                if float(right) == 0:
                    raise LoxRuntimeError(
                        expr.operator,
                        "Division by zero!",
                    )
                return float(left) / float(right)
            case TokenType.STAR:
                self.check_number_operands(expr.operator, left, right)
                return float(left) * float(right)

    def visit_grouping_expr(self, expr: expr_ast.Grouping) -> typing.Any:
        return expr.expr.accept(self)

    def visit_literal_expr(self, expr: expr_ast.Literal) -> typing.Any:
        return expr.value

    def visit_unary_expr(self, expr: expr_ast.Unary) -> typing.Any:
        right = self.evaluate(expr.right)

        if expr.operator.token_type is TokenType.MINUS:
            self.check_number_operand(expr.operator, right)
            return -float(right)
        elif expr.operator.token_type is TokenType.BANG:
            return not self.is_truthy(right)

        # pragma: no cover
        raise LoxRuntimeError(
            expr.operator,
            f'Unknown operator for unary operation -- "{expr.operator.lexeme}"!',
        )

    @staticmethod
    def is_truthy(right: typing.Any) -> bool:
        if right is None:
            return False
        elif type(right) is bool:
            return bool(right)
        else:
            return True

    @staticmethod
    def is_number(value: typing.Any) -> bool:
        return (type(value) is int) or (type(value) is float)

    @staticmethod
    def check_number_operand(op: Token, operand: typing.Any) -> None:
        if Interpreter.is_number(operand):
            return
        raise LoxRuntimeError(op, "Operand must be a number.")

    @staticmethod
    def check_number_operands(op: Token, left, right: typing.Any) -> None:
        if Interpreter.is_number(left) and Interpreter.is_number(right):
            return
        raise LoxRuntimeError(op, "Operands must be a numbers.")

    @staticmethod
    def stringify(value: typing.Any) -> str:
        if value is None:
            return "nil"

        if type(value) is float and float(value).is_integer():
            return str(int(value))

        return str(value)
