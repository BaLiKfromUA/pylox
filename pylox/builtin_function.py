import time
import typing

from pylox.runtime_entity import LoxCallable

if typing.TYPE_CHECKING:
    from pylox.interpreter import Interpreter


class Clock(LoxCallable):
    def call(
        self, interpreter: "Interpreter", args: typing.List[typing.Any]
    ) -> typing.Any:
        return time.time()

    def arity(self) -> int:
        return 0

    def __str__(self) -> str:
        return "<native fn>"


class Input(LoxCallable):
    def call(
        self, interpreter: "Interpreter", args: typing.List[typing.Any]
    ) -> typing.Any:
        return input()

    def arity(self) -> int:
        return 0

    def __str__(self) -> str:
        return "<native fn>"


class Len(LoxCallable):
    def call(
        self, interpreter: "Interpreter", args: typing.List[typing.Any]
    ) -> typing.Any:
        return len(args[0])

    def arity(self) -> int:
        return 1

    def __str__(self) -> str:
        return "<native fn>"


FUNCTIONS_MAPPING = {"clock": Clock(), "input": Input(), "len": Len()}
