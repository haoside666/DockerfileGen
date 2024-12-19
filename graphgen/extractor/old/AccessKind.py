from graphgen.extractor.util_standard import standard_eq, standard_repr
from enum import Enum


class AccessKindEnum(Enum):
    CONFIG_INPUT = 0
    STREAM_INPUT = 1
    OTHER_INPUT = 2
    CONFIG_OUTPUT = 3
    STREAM_OUTPUT = 4
    OTHER_OUTPUT = 5
    CONFIG_INPUT_OR_OUTPUT = 6


class AccessKind:
    def __init__(self, kind) -> None:
        self.kind: AccessKindEnum = kind

    def __repr__(self):
        return standard_repr(self)

    def __eq__(self, other) -> bool:
        return standard_eq(self, other)

    def is_config_input(self) -> bool:
        return self.kind == AccessKindEnum.CONFIG_INPUT

    def is_stream_input(self) -> bool:
        return self.kind == AccessKindEnum.STREAM_INPUT

    def is_other_input(self) -> bool:
        return self.kind == AccessKindEnum.OTHER_INPUT

    def is_any_input(self):
        return self.is_config_input() or self.is_stream_input() or self.is_other_input() or self.is_config_input_or_output()

    def is_config_output(self):
        return self.kind == AccessKindEnum.CONFIG_OUTPUT

    def is_stream_output(self):
        return self.kind == AccessKindEnum.STREAM_OUTPUT

    def is_other_output(self):
        return self.kind == AccessKindEnum.OTHER_OUTPUT

    def is_config_input_or_output(self):
        return self.kind == AccessKindEnum.CONFIG_INPUT_OR_OUTPUT

    def is_any_output(self):
        return self.is_stream_output() or self.is_other_output() or self.is_config_output() or self.is_config_input_or_output()


def make_config_input() -> AccessKind:
    return AccessKind(AccessKindEnum.CONFIG_INPUT)


def make_stream_input() -> AccessKind:
    return AccessKind(AccessKindEnum.STREAM_INPUT)


def make_other_input() -> AccessKind:
    return AccessKind(AccessKindEnum.OTHER_INPUT)


def make_config_output() -> AccessKind:
    return AccessKind(AccessKindEnum.CONFIG_OUTPUT)


def make_stream_output() -> AccessKind:
    return AccessKind(AccessKindEnum.STREAM_OUTPUT)


def make_other_output() -> AccessKind:
    return AccessKind(AccessKindEnum.OTHER_OUTPUT)


def make_config_input_or_output() -> AccessKind:
    return AccessKind(AccessKindEnum.CONFIG_INPUT_OR_OUTPUT)


def get_access_from_string(value: str) -> AccessKind:
    if value == "CONFIG_INPUT":
        return make_config_input()
    elif value == "STREAM_INPUT":
        return make_stream_input()
    elif value == "OTHER_INPUT":
        return make_other_input()
    elif value == "CONFIG_OUTPUT":
        return make_config_output()
    elif value == "STREAM_OUTPUT":
        return make_stream_output()
    elif value == "OTHER_OUTPUT":
        return make_other_output()
    elif value == "CONFIG_INPUT_OR_OUTPUT":
        return make_config_input_or_output()
    else:
        raise Exception("unknown option for access kind")
