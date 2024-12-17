import json

from dockdepend.util import standard_repr, standard_eq, return_empty_list_if_none_else_itself
from typing import List, Dict, Union, Tuple
from copy import deepcopy

CMD_TYPE = Union[str, List[str]]


class PrimitiveFeature:
    def __init__(self, var_p_list: List[Tuple[str, str]] = None, command: CMD_TYPE = None,
                 redir_input_list: List[str] = None, redir_output_list: List[str] = None,
                 other_list: List[str] = None, var_c_list: List[str] = None) -> None:
        self.var_p_list: List[Tuple[str, str]] = return_empty_list_if_none_else_itself(var_p_list)
        self.command: CMD_TYPE = return_empty_list_if_none_else_itself(command)
        self.redir_input_list: List[str] = return_empty_list_if_none_else_itself(redir_input_list)
        self.redir_output_list: List[str] = return_empty_list_if_none_else_itself(redir_output_list)
        self.other_list: List[str] = return_empty_list_if_none_else_itself(other_list)
        self.var_c_list: List[str] = return_empty_list_if_none_else_itself(var_c_list)

    def json(self) -> str:
        d = dict()
        d["var_p_list"] = self.var_p_list
        d["command"] = self.command
        d["redir_input_list"] = self.redir_input_list
        d["redir_output_list"] = self.redir_output_list
        d["other_list"] = self.other_list
        d["var_c_list"] = self.var_c_list
        return json.dumps(d) + "\n"

    def __repr__(self):
        return standard_repr(self)

    def __eq__(self, other) -> bool:
        return standard_eq(self, other)

    def split_other_list_to_two_part(self) -> Tuple[List[str], List[str]]:
        one_part: list[str] = []
        two_part: list[str] = []
        other_list: list = list(set(self.other_list))
        for item in other_list:
            if "/" in item:
                one_part.append(item)
            else:
                two_part.append(item)
        return one_part, two_part
