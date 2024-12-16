from dockdepend.extractor.util_standard import standard_repr, standard_eq
from dockdepend.extractor.datatypes.CommandInvocationInitial import CommandInvocationInitial
from copy import deepcopy


class CommandInvocationAfterIOChange(CommandInvocationInitial):
    def __init__(self, cmd_inv: CommandInvocationInitial) -> None:
        super().__init__(cmd_inv.cmd_name, deepcopy(cmd_inv.flag_option_list), deepcopy(cmd_inv.operand_list))

    def __repr__(self):
        return standard_repr(self)

    def __eq__(self, other):
        return standard_eq(self, other)
