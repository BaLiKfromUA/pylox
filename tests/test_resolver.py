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


@patch("pylox.interpreter")
def test_if_resolver_handles_break_outside_of_the_loop(interpreter):
    # GIVEN
    src = "break;"
    # WHEN
    with pytest.raises(LoxParseError) as err:
        run_resolver(src, interpreter)
    # THEN
    assert not interpreter.called
    assert "Must be inside a loop to use 'break'." in err.value.message


@patch("pylox.interpreter")
def test_if_resolver_handles_return_outside_of_the_loop(interpreter):
    # GIVEN
    src = """
            fun notAMethod() {
                print this;
            }
          """
    # WHEN
    with pytest.raises(LoxParseError) as err:
        run_resolver(src, interpreter)
    # THEN
    assert "Can't use 'this' outside of a class." in err.value.message


@patch("pylox.interpreter")
def test_if_resolver_handles_return_inside_init(interpreter):
    # GIVEN
    valid_code = """
        class Foo {
            init() {
                return;
            }
        }
    """

    invalid_code = """
        class Foo {
            init() {
                return 42;
            }
        }
    """

    # WHEN
    run_resolver(valid_code, interpreter)  # no errors
    with pytest.raises(LoxParseError) as err:
        run_resolver(invalid_code, interpreter)

    # THEN
    assert "Can't return a value from an initializer." in err.value.message


@patch("pylox.interpreter")
def test_if_resolver_checks_class_inheritance_from_itself(interpreter):
    # GIVEN
    src = "class Oops < Oops {}"
    # WHEN
    with pytest.raises(LoxParseError) as err:
        run_resolver(src, interpreter)

    # THEN
    assert "A class can't inherit from itself." in err.value.message
