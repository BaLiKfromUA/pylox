import io
import os
from contextlib import redirect_stdout, redirect_stderr
from pathlib import Path

import pytest

from pylox.cli import Lox


def prepare_list_of_test_files():
    start_path = f"{os.path.dirname(os.path.realpath(__file__))}/data/"
    return [
        pytest.param(
            str(path).replace(start_path, ""),
            marks=getattr(pytest.mark, str(path).replace(start_path, "")),
        )
        for path in Path(start_path).rglob("*.lox")
    ]


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
