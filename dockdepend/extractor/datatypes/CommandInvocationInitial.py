import json
from typing import List

from dockdepend.extractor.datatypes.BasicDatatypes import FlagOption, Operand
from dockdepend.extractor.util_standard import standard_repr, standard_eq


class CommandInvocationInitial:
    def __init__(self, cmd_name: str, flag_option_list: List[FlagOption], operand_list: List[Operand]) -> None:
        self.cmd_name: str = cmd_name
        self.flag_option_list: List[FlagOption] = flag_option_list
        self.operand_list: List[Operand] = operand_list

    def __repr__(self):
        return standard_repr(self)

    def __eq__(self, other):
        return standard_eq(self, other)

    def to_dict(self):
        return {
            "cmd_name": self.cmd_name,
            "flag_option_list": [item.to_json() for item in self.flag_option_list],
            "operand_list": [item.to_json() for item in self.operand_list]
        }

    def does_operand_list_contain(self, list_operand: List[str]) -> bool:
        operand_list_str = " ".join([item.get_name() for item in self.operand_list])
        for item in list_operand:
            if item in operand_list_str:
                return True
        return False
