import io
import os
from contextlib import redirect_stdout, redirect_stderr
from pathlib import Path

import pytest

from pylox.cli import Lox

EXPECTED_TO_FAIL = ["block/empty.lox", "assignment/to_this.lox"]


def prepare_list_of_test_files():
    start_path = f"{os.path.dirname(os.path.realpath(__file__))}/data/"
    tests = [
        str(path).replace(start_path, "")
        for path in Path(start_path).rglob("*.lox")
    ]
    tests_with_marks = [
        pytest.param(test, marks=[getattr(pytest.mark, test)])
        for test in tests
    ]
    for test in tests_with_marks:
        if test.values[0] in EXPECTED_TO_FAIL:
            test.marks.append(pytest.mark.xfail)

    return tests_with_marks


def parse_test_file(filename: Path) -> list[str]:
    with open(filename) as f:
        lines = [line.rstrip("\n") for line in f]
        return [
            line.split("// expect:")[1].strip()
            for line in lines
            if "// expect" in line
        ]


@pytest.mark.parametrize("file", prepare_list_of_test_files())
def test_if_interpreter_works_as_expected(file: str) -> None:
    # GIVEN
    filename = Path(file).absolute()
    expected = parse_test_file(filename)
    with io.StringIO() as buf, redirect_stdout(buf), redirect_stderr(buf):
        try:
            # WHEN
            Lox().run_file(filename)
        except SystemExit:
            pass
        finally:
            output = buf.getvalue()
            actual = output.split("\n")[:-1]  # remove last '' element
    # THEN
    assert actual == expected
