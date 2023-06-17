from unittest.mock import patch

import pytest

from pylox.error import LoxParseError
from pylox.interpreter import Interpreter
from pylox.parser import Parser
from pylox.resolver import Resolver
from pylox.scanner import Scanner


def run_resolver(src: str, interpreter: Interpreter):
    tokens = Scanner(src).scan_tokens()
    ast = Parser(tokens).parse()
    resolver = Resolver(interpreter)
    resolver.resolve(ast)


@patch("pylox.interpreter")
def test_if_local_variable_reads_itself_during_init_then_resolver_produces_error(
    interpreter,
):
    # GIVEN
    src = "{var a = a;}"
    # WHEN
    with pytest.raises(LoxParseError) as err:
        run_resolver(src, interpreter)
    # THEN
    assert not interpreter.called
    assert (
        "Can't read local variable in its own initializer."
        in err.value.message
    )


@patch("pylox.interpreter")
def test_if_resolver_finds_return_out_of_the_function(interpreter):
    # GIVEN
    src = 'return "at top level";'
    # WHEN
    with pytest.raises(LoxParseError) as err:
        run_resolver(src, interpreter)
    # THEN
    assert not interpreter.called
    assert "Can't return from top-level code." in err.value.message
