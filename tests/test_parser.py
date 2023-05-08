import pytest

from pylox.error import LoxParseError
from pylox.experimental.ast_printer import AstPrinter
from pylox.parser import Parser
from pylox.scanner import Scanner


def test_if_parser_produces_valid_ast() -> None:
    # GIVEN
    src = "-123 * (45.67)"
    # WHEN
    tokens = Scanner(src).scan_tokens()
    ast = Parser(tokens).expression()
    result = AstPrinter().print_expr(ast)
    # THEN
    assert result == "(* (- 123) (group 45.67))"


def test_if_parser_handles_unclosed_paren() -> None:
    # GIVEN
    src = "-123 * (45.67"
    # WHEN
    tokens = Scanner(src).scan_tokens()
    with pytest.raises(LoxParseError) as err:
        Parser(tokens).expression()
    # THEN
    assert "Expect ')' after expression." in err.value.message


def test_if_parser_handles_empty_right_hand_operand_inside_binary_expression() -> (
    None
):
    # GIVEN
    src = "123 * "
    # WHEN
    tokens = Scanner(src).scan_tokens()
    with pytest.raises(LoxParseError) as err:
        Parser(tokens).expression()
    # THEN
    assert "Expect expression" in err.value.message
