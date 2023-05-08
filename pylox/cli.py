import sys
import typing as t
from parser import Parser
from pathlib import Path

import typer
from rich import print
from rich.prompt import Prompt
from scanner import Scanner

from pylox.error import LoxException, LoxRuntimeError, LoxSyntaxError
from pylox.experimental.ast_printer import AstPrinter

pylox_cli = typer.Typer()
Prompt.prompt_suffix = ""  # Get rid of the default colon suffix


class Lox:
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
        try:
            tokens = Scanner(src).scan_tokens()
            ast = Parser(tokens, self.report_error).parse()
            if ast is not None:
                print(AstPrinter().print_expr(ast))  # todo: replace
        except LoxSyntaxError as e:
            self.report_error(e)
        except LoxRuntimeError as e:
            self.report_runtime_error(e)

    @staticmethod
    def _build_error_string(err: LoxException) -> str:
        return f"{err.line + 1}: [bold red]{err.message}[/bold red]"

    def report_error(self, err: LoxException) -> None:
        print(self._build_error_string(err))
        self.had_error = True

    def report_runtime_error(self, err: LoxRuntimeError) -> None:
        print(self._build_error_string(err))
        self.had_error = True
        self.had_runtime_error = True


@pylox_cli.command()
def main(
    lox_script: t.Optional[Path] = typer.Argument(default=None),
) -> None:  # pragma: no cover
    lox = Lox()
    if not lox_script:
        lox.run_prompt()
    else:
        lox.run_file(lox_script)
