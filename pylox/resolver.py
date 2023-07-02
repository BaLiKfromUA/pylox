import typing
from enum import Enum, auto

import pylox.expr as expr_ast
import pylox.stmt as stmt_ast
from pylox.error import LoxParseError
from pylox.expr import Expr, ExprVisitor
from pylox.interpreter import Interpreter
from pylox.scanner import Token
from pylox.stmt import Stmt, StmtVisitor


class FunctionType(Enum):
    NONE = (auto(),)
    FUNCTION = auto()


class Resolver(ExprVisitor, StmtVisitor):
    def __init__(self, interpreter: Interpreter):
        self.interpreter = interpreter
        self.scopes: typing.List[typing.Dict[str, bool]] = []
        self.current_function = FunctionType.NONE
        self.loop_depth = 0

    def begin_scope(self) -> None:
        self.scopes.append({})

    def end_scope(self) -> None:
        self.scopes.pop()

    def declare(self, identifier: Token) -> None:
        if len(self.scopes) == 0:
            return
        scope = self.scopes[-1]
        scope[identifier.lexeme] = False

    def define(self, identifier: Token) -> None:
        if len(self.scopes) == 0:
            return
        scope = self.scopes[-1]
        scope[identifier.lexeme] = True

    def resolve(self, statements: list[Stmt]) -> None:
        for statement in statements:
            self.resolve_ast_node(statement)

    def resolve_ast_node(self, node: Stmt | Expr) -> None:
        node.accept(self)

    def resolve_local(self, expr: Expr, name: Token) -> None:
        for i in range(len(self.scopes) - 1, -1, -1):
            if name.lexeme in self.scopes[i].keys():
                self.interpreter.resolve(expr, len(self.scopes) - 1 - i)
                return

    def resolve_function(
        self, function: stmt_ast.Function, fun_type: FunctionType
    ) -> None:
        parent_fun = self.current_function
        self.current_function = fun_type
        self.begin_scope()
        for param in function.params:
            self.declare(param)
            self.define(param)
        self.resolve(function.body)
        self.end_scope()
        self.current_function = parent_fun

    def visit_assign_expr(self, expr: expr_ast.Assign) -> typing.Any:
        self.resolve_ast_node(expr.value)
        self.resolve_local(expr, expr.name)
        return None

    def visit_binary_expr(self, expr: expr_ast.Binary) -> typing.Any:
        self.resolve_ast_node(expr.left)
        self.resolve_ast_node(expr.right)
        return None

    def visit_call_expr(self, expr: expr_ast.Call) -> typing.Any:
        self.resolve_ast_node(expr.callee)
        for arg in expr.arguments:
            self.resolve_ast_node(arg)
        return None

    def visit_grouping_expr(self, expr: expr_ast.Grouping) -> typing.Any:
        self.resolve_ast_node(expr.expr)
        return None

    def visit_literal_expr(self, expr: expr_ast.Literal) -> typing.Any:
        # do nothing
        return None

    def visit_logical_expr(self, expr: expr_ast.Logical) -> typing.Any:
        self.resolve_ast_node(expr.left)
        self.resolve_ast_node(expr.right)
        return None

    def visit_unary_expr(self, expr: expr_ast.Unary) -> typing.Any:
        self.resolve_ast_node(expr.right)
        return None

    def visit_variable_expr(self, expr: expr_ast.Variable) -> typing.Any:
        if (
            len(self.scopes) > 0
            and self.scopes[-1].get(expr.name.lexeme) is False
        ):
            raise LoxParseError(
                expr.name, "Can't read local variable in its own initializer."
            )
        self.resolve_local(expr, expr.name)
        return None

    def visit_block_stmt(self, stmt: stmt_ast.Block) -> typing.Any:
        self.begin_scope()
        self.resolve(stmt.statements)
        self.end_scope()
        return None

    def visit_expression_stmt(self, stmt: stmt_ast.Expression) -> typing.Any:
        self.resolve_ast_node(stmt.expr)
        return None

    def visit_function_stmt(self, stmt: stmt_ast.Function) -> typing.Any:
        self.declare(stmt.name)
        # Unlike variables, though, we define the name eagerly,
        # before resolving the function’s body.
        # This lets a function recursively refer to itself inside its own body.
        self.define(stmt.name)
        self.resolve_function(stmt, FunctionType.FUNCTION)
        return None

    def visit_if_stmt(self, stmt: stmt_ast.If) -> typing.Any:
        self.resolve_ast_node(stmt.condition)
        self.resolve_ast_node(stmt.then_branch)
        if stmt.else_branch is not None:
            self.resolve_ast_node(stmt.else_branch)
        return None

    def visit_print_stmt(self, stmt: stmt_ast.Print) -> typing.Any:
        self.resolve_ast_node(stmt.expr)
        return None

    def visit_return_stmt(self, stmt: stmt_ast.Return) -> typing.Any:
        if self.current_function is FunctionType.NONE:
            raise LoxParseError(
                stmt.keyword, "Can't return from top-level code."
            )

        if stmt.value is not None:
            self.resolve_ast_node(stmt.value)
        return None

    def visit_var_stmt(self, stmt: stmt_ast.Var) -> typing.Any:
        self.declare(stmt.name)
        if stmt.initializer is not None:
            self.resolve_ast_node(stmt.initializer)
        self.define(stmt.name)
        return None

    def visit_while_stmt(self, stmt: stmt_ast.While) -> typing.Any:
        self.resolve_ast_node(stmt.condition)
        self.loop_depth += 1
        self.resolve_ast_node(stmt.body)
        self.loop_depth -= 1
        return None

    def visit_break_stmt(self, stmt: stmt_ast.Break) -> typing.Any:
        if self.loop_depth == 0:
            raise LoxParseError(
                stmt.keyword, "Must be inside a loop to use 'break'."
            )
        return None

    def visit_class_stmt(self, stmt: stmt_ast.Class) -> typing.Any:
        self.declare(stmt.name)
        self.define(stmt.name)
        return None
