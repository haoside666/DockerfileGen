from typing import Union
from dockdepend.extractor.util_standard import standard_eq, standard_repr
from enum import Enum
from abc import ABC, abstractmethod


# note that we have individual classes since aliasing does not provide as much support
class BaseClassForBasicDatatypes(ABC):
    def __repr__(self) -> str:
        return standard_repr(self)

    def __eq__(self, other) -> bool:
        return standard_eq(self, other)

    @abstractmethod
    def get_name(self) -> str:
        pass


class FileName(BaseClassForBasicDatatypes):
    def __init__(self, name: str) -> None:
        self.name = name

    def get_name(self) -> str:
        return self.name


class StdDescriptorEnum(Enum):
    STDIN = 0
    STDOUT = 1
    STDERR = 2


class StdDescriptor(BaseClassForBasicDatatypes):
    def __init__(self, name: StdDescriptorEnum) -> None:
        self.name = name

    def get_name(self) -> str:
        return str(self.name)

    def get_type(self) -> StdDescriptorEnum:
        return self.name


def get_stdin_fd() -> StdDescriptor:
    return StdDescriptor(StdDescriptorEnum.STDIN)


def get_stdout_fd() -> StdDescriptor:
    return StdDescriptor(StdDescriptorEnum.STDOUT)


def get_stderr_fd() -> StdDescriptor:
    return StdDescriptor(StdDescriptorEnum.STDERR)


FileNameOrStdDescriptor = Union[FileName, StdDescriptor]


class ArgStringType(BaseClassForBasicDatatypes):
    def __init__(self, name: str) -> None:
        self.name = name

    def get_name(self) -> str:
        return self.name


OptionArg = Union[str, ArgStringType, FileNameOrStdDescriptor]


class Flag(BaseClassForBasicDatatypes):
    def __init__(self, name: str) -> None:
        self.flag_name = name

    def get_name(self) -> str:
        return self.flag_name

    def to_json(self):
        return self.flag_name


class Option(BaseClassForBasicDatatypes):
    def __init__(self, name: str, option_arg: OptionArg) -> None:
        self.option_name = name
        self.option_arg: OptionArg = option_arg

    def get_name(self) -> str:
        return self.option_name

    def get_arg(self) -> str:
        if isinstance(self.option_arg, str):
            return self.option_arg
        else:
            return self.option_arg.get_name()

    def to_json(self):
        return [
            self.get_name(),
            self.get_arg()
        ]


FlagOption = Union[Flag, Option]


# Note difference between Option argument and Operand after parsing:
# for option arguments, we know which is a filename; for operands, we don't

class Operand(BaseClassForBasicDatatypes):
    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self) -> str:
        return f'{self.name}'

    def get_name(self) -> str:
        return self.name

    def contains_new_line(self):
        name_as_string = str(self.name)
        return name_as_string.find(r"\n") > 0

    def contains_null_char(self):
        name_as_string = str(self.name)
        return name_as_string.find(r"\0") > 0

    def to_arg_string_type(self):
        return ArgStringType(self.name)

    def to_json(self):
        return self.name

# class WhichClassForArg(Enum):
#     FILESTD = 'filestd'
#     ARGSTRING = 'argstring'
#     PLAINSTRING = 'str'
