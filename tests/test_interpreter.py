import io
from contextlib import redirect_stdout
from pathlib import Path

import pytest

from pylox.cli import Lox


def parse_test_file(filename: Path) -> list[str]:
    expected: list[str] = []
    with open(filename) as f:
        lines = [line.rstrip("\n") for line in f]
        for line in lines:
            if line.startswith("// expect"):
                expected.append(line.split(":")[1])

    return expected


@pytest.mark.parametrize("file", ["print_basic_expr.lox"])
def test_if_interpreter_works_as_expected(file: str) -> None:
    # GIVEN
    filename = Path(file).absolute()
    expected = parse_test_file(filename)
    # WHEN
    with io.StringIO() as buf, redirect_stdout(buf):
        Lox().run_file(filename)
        output = buf.getvalue()
        actual = output.split("\n")[:-1]  # remove last '' element
    # THEN
    assert actual == expected
