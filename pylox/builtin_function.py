import time
import typing

from pylox.runtime_entity import LoxCallable


class Clock(LoxCallable):
    def call(self, interpreter, args) -> typing.Any:
        return time.time()

    def arity(self) -> int:
        return 0


class Input(LoxCallable):
    def call(self, interpreter, args) -> typing.Any:
        return input()

    def arity(self) -> int:
        return 0


class Len(LoxCallable):
    def call(self, interpreter, args) -> typing.Any:
        return len(args[0])

    def arity(self) -> int:
        return 1


FUNCTIONS_MAPPING = {"clock": Clock(), "input": Input(), "len": Len()}
