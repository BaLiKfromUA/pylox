import io
import os
from contextlib import redirect_stdout, redirect_stderr
from pathlib import Path
from unittest import mock

import pytest

from pylox.cli import Lox

EXPECTED_TO_FAIL = [
    "assignment/to_this.lox",
    "number/trailing_dot.lox",
    "number/decimal_point_at_eof.lox",
]

IGNORE = ["custom/input.lox"]


def prepare_list_of_test_files():
    start_path = f"{os.path.dirname(os.path.realpath(__file__))}/data/"
    tests = [
        str(path).replace(start_path, "")
        for path in Path(start_path).rglob("*.lox")
    ]
    tests_with_marks_and_filtered = [
        pytest.param(test, marks=[getattr(pytest.mark, test)])
        for test in tests
        if not (test in IGNORE)
    ]
    for test in tests_with_marks_and_filtered:
        if test.values[0] in EXPECTED_TO_FAIL:
            test.marks.append(pytest.mark.xfail)

    return tests_with_marks_and_filtered


def parse_test_file(filename: Path) -> list[str]:
    with open(filename) as f:
        lines = [line.rstrip("\n") for line in f]
        return [
            line.split("// expect:")[1].strip()
            for line in lines
            if "// expect" in line
        ]


def run_file(filename: Path) -> list[str]:
    with io.StringIO() as buf, redirect_stdout(buf), redirect_stderr(buf):
        try:
            Lox().run_file(filename)
        except SystemExit:
            pass
        finally:
            output = buf.getvalue()
            return output.split("\n")[:-1]  # remove last '' element


@pytest.mark.parametrize("file", prepare_list_of_test_files())
def test_if_interpreter_works_as_expected(file: str) -> None:
    # GIVEN
    filename = Path(file).absolute()
    expected = parse_test_file(filename)
    # WHEN
    actual = run_file(filename)
    # THEN
    assert actual == expected


@mock.patch(
    "builtins.input",
    side_effect=[
        'var s = "Hello, World!";',
        "print s;",
        "print no_var;",
        "2 + 2 * 2",
        "exit",
    ],
)
def test_if_interpreter_works_as_expected_in_repl_mode(ignored) -> None:
    expected = ["Hello, World!", "line 1: Undefined variable no_var.", "6"]

    with io.StringIO() as buf, redirect_stdout(buf), redirect_stderr(buf):
        # WHEN
        Lox().run_prompt()
        output = buf.getvalue()
        actual = [
            line.replace(">", "").strip() for line in output.split("\n")[:-1]
        ]

    # THEN
    assert actual == expected


@mock.patch("time.time", return_value=42)
def test_if_builtin_functions_work_as_expected_without_args(mock_time) -> None:
    # GIVEN
    src = "print clock();"
    # WHEN
    with io.StringIO() as buf, redirect_stdout(buf), redirect_stderr(buf):
        Lox().run(src)
        output = buf.getvalue()
    # THEN
    mock_time.assert_called_once()
    assert output == "42\n"


@mock.patch("builtins.input", return_value="test")
def test_if_builtin_functions_work_as_expected_with_args(mock_input) -> None:
    # GIVEN
    file = "custom/input.lox"
    filename = Path(file).absolute()
    # WHEN
    actual = run_file(filename)
    # THEN
    mock_input.assert_called_once()
    assert len(actual) == 1
    assert actual[0] == "4"
