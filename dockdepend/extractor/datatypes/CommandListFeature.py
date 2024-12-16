from typing import List
from dockdepend.extractor.util_standard import standard_repr, standard_eq
from dockdepend.extractor.datatypes.CommandInvocationFeature import CommandInvocationFeature


class CommandListFeature:
    def __init__(self, cmd_name_list: List, input_list: List, output_list: List, pkg_list: List, other_list: List,
                 user_list: List) -> None:
        self.cmd_name_list: List[str] = cmd_name_list
        self.input_list: List[str] = input_list
        self.output_list: List[str] = output_list
        self.pkg_list: List[str] = pkg_list
        self.other_list: List[str] = other_list
        self.user_list: List[str] = user_list

    def __repr__(self):
        return standard_repr(self)

    def __eq__(self, other):
        return standard_eq(self, other)


def make_command_list_feature(cmd_inv_feature_list: List[CommandInvocationFeature]):
    command_list: List[str] = []
    input_list: List = []
    output_list: List = []
    pkg_list: List = []
    other_list: List = []
    user_list: List = []
    for item in cmd_inv_feature_list:
        command_list.append(item.cmd_name)
        input_list.extend(item.input_list)
        output_list.extend(item.output_list)
        pkg_list.extend(item.pkg_list)
        other_list.extend(item.other_list)
        user_list.extend(item.user_list)
    return CommandListFeature(command_list, input_list, output_list, pkg_list, other_list, user_list)
