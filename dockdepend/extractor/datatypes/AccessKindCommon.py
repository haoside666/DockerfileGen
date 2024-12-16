from dockdepend.extractor.util_standard import standard_eq, standard_repr
from enum import Enum


class AccessKindCommonEnum(Enum):
    CONFIG_INPUT = 0
    CONFIG_OUTPUT = 1
    CONFIG_INPUT_OR_OUTPUT = 2
    OTHER_INPUT = 3
    OTHER_OUTPUT = 4
    OTHER_IO = 5


class AccessKindCommon:
    def __init__(self, kind) -> None:
        self.kind: AccessKindCommonEnum = kind

    def __repr__(self):
        return standard_repr(self)

    def __eq__(self, other) -> bool:
        return standard_eq(self, other)

    def is_config_input(self) -> bool:
        return self.kind == AccessKindCommonEnum.CONFIG_INPUT

    def is_config_output(self) -> bool:
        return self.kind == AccessKindCommonEnum.CONFIG_OUTPUT

    def is_config_input_or_output(self):
        return self.kind == AccessKindCommonEnum.CONFIG_INPUT_OR_OUTPUT

    def is_other_input(self) -> bool:
        return self.kind == AccessKindCommonEnum.OTHER_INPUT

    def is_other_output(self) -> bool:
        return self.kind == AccessKindCommonEnum.OTHER_OUTPUT

    def is_other_io(self) -> bool:
        return self.kind == AccessKindCommonEnum.OTHER_IO

    def is_any_input(self):
        return self.is_config_input() or self.is_other_input() or self.is_other_io() or self.is_config_input_or_output()

    def is_any_output(self):
        return self.is_other_output() or self.is_config_output() or self.is_other_io() or self.is_config_input_or_output()


def make_config_input() -> AccessKindCommon:
    return AccessKindCommon(AccessKindCommonEnum.CONFIG_INPUT)


def make_config_output() -> AccessKindCommon:
    return AccessKindCommon(AccessKindCommonEnum.CONFIG_OUTPUT)


def make_config_input_or_output() -> AccessKindCommon:
    return AccessKindCommon(AccessKindCommonEnum.CONFIG_INPUT_OR_OUTPUT)


def make_other_input() -> AccessKindCommon:
    return AccessKindCommon(AccessKindCommonEnum.OTHER_INPUT)


def make_other_output() -> AccessKindCommon:
    return AccessKindCommon(AccessKindCommonEnum.OTHER_OUTPUT)


def make_other_io() -> AccessKindCommon:
    return AccessKindCommon(AccessKindCommonEnum.OTHER_IO)


def get_access_from_string(value: str) -> AccessKindCommon:
    if value == "CONFIG_INPUT":
        return make_config_input()
    elif value == "CONFIG_OUTPUT":
        return make_config_output()
    elif value == "CONFIG_INPUT_OR_OUTPUT":
        return make_config_input_or_output()
    elif value == "OTHER_INPUT":
        return make_other_input()
    elif value == "OTHER_OUTPUT":
        return make_other_output()
    elif value == "OTHER_IO":
        return make_other_io()
    else:
        raise Exception("unknown option for access kind")


class WhichClassForFeature(Enum):
    FILESTD = 'filestd'
    USER = 'user'
    PKG = 'PKG'
    OTHER = 'other'
    ARGSTRING = 'argstring'
    PLAINSTRING = 'str'
