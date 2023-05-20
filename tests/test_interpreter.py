import io
import os
from contextlib import redirect_stdout
from pathlib import Path

import pytest

from pylox.cli import Lox


def prepare_list_of_test_files() -> list[str]:
    start_path = f"{os.path.dirname(os.path.realpath(__file__))}/data/"
    return [
        str(path).replace(start_path, "")
        for path in Path(start_path).rglob("*.lox")
    ]


def parse_test_file(filename: Path) -> list[str]:
    with open(filename) as f:
        lines = [line.rstrip("\n") for line in f]
        return [
            line.split(":")[1]
            for line in lines
            if line.strip().startswith("// expect")
        ]


@pytest.mark.parametrize("file", prepare_list_of_test_files())
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
