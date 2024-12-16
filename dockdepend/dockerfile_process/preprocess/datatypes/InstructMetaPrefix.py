from dockdepend.util import standard_eq
from .Operand import Operand


# for use as a node in a dependency graph
class InstructMetaPrefix:
    def __init__(self, cmd_name: str, operand: Operand = None) -> None:
        self.cmd_name = cmd_name
        self.operand = operand

    def __repr__(self):
        return f'CommandMeta({self.cmd_name.__repr__()}, {self.operand.__repr__()}) '

    def __str__(self):
        return f'cmd_name: {self.cmd_name}, {self.operand.__str__()}'

    def __eq__(self, other) -> bool:
        return standard_eq(self, other)
