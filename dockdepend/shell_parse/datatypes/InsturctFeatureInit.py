from dockdepend.util import standard_repr, standard_eq, return_empty_list_if_none_else_itself
from typing import List, Union, Tuple

CMD_TYPE = Union[List[str], List[List[str]]]


class InstructFeatureInit:
    def __init__(self, var_p_list: List[Tuple[str, str]] = None, command_list: CMD_TYPE = None,
                 redir_input_list: List[str] = None, redir_output_list: List[str] = None, var_c_list: List[str] = None,
                 other_list: List[str] = None) -> None:
        self.var_p_list: List[Tuple[str, str]] = return_empty_list_if_none_else_itself(var_p_list)
        self.command_list: CMD_TYPE = return_empty_list_if_none_else_itself(command_list)
        self.redir_input_list: List[str] = return_empty_list_if_none_else_itself(redir_input_list)
        self.redir_output_list: List[str] = return_empty_list_if_none_else_itself(redir_output_list)
        self.var_c_list: List[str] = return_empty_list_if_none_else_itself(var_c_list)
        self.other_list: List[str] = return_empty_list_if_none_else_itself(other_list)

    def __repr__(self):
        return standard_repr(self)

    def __eq__(self, other) -> bool:
        return standard_eq(self, other)

    def to_dict(self):
        json_data = dict()
        json_data["VarPSet"] = list(set(self.var_p_list))
        json_data["VarCSet"] = list(set(self.var_c_list))
        json_data["CommandSet"] = self.command_list
        json_data["RedirectInputSet"] = list(set(self.redir_input_list))
        json_data["RedirectOutputSet"] = list(set(self.redir_output_list))
        other_set = set(self.other_list)
        other_set.discard("$(command)")
        other_set.discard('"$(command)"')
        json_data["OtherSet"] = list(other_set)
        return json_data

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
