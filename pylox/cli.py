import sys
import typing as t
from pathlib import Path

import typer
from rich import print
from rich.prompt import Prompt

from pylox.error import LoxException, LoxRuntimeError

pylox_cli = typer.Typer()
Prompt.prompt_suffix = ""  # Get rid of the default colon suffix


class Lox:  # pragma: no cover
    def __init__(self) -> None:
        self.had_error = False
        self.had_runtime_error = False

    def run_file(self, src_filepath: Path) -> None:
        src = src_filepath.read_text()
        self.run(src)

        if self.had_error:
            sys.exit(65)

        if self.had_runtime_error:
            sys.exit(70)

    def run_prompt(self) -> None:
        while True:
            line = Prompt.ask("> ")

            if line == "exit":
                break

            self.run(line)

            # Reset these so we can stay in the REPL unhindered
            self.had_error = False
            self.had_runtime_error = False

    def run(self, src: str) -> None:
        pass

    def _build_error_string(self, err: LoxException) -> str:
        return f"{err.line + 1}: [bold red]{err}[/bold red]"

    def report_error(self, err: LoxException) -> None:
        print(self._build_error_string(err))
        self.had_error = True

    def report_runtime_error(self, err: LoxRuntimeError) -> None:
        print(self._build_error_string(err))
        self.had_error = True
        self.had_runtime_error = True


@pylox_cli.command()
def main(lox_script: t.Optional[Path] = typer.Argument(default=None)) -> None:  # pragma: no cover
    lox = Lox()
    if not lox_script:
        lox.run_prompt()
    else:
        lox.run_file(lox_script)
