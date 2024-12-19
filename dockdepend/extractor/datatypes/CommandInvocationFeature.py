import json
from typing import List, Union

from dockdepend.util import return_empty_list_if_none_else_itself

from dockdepend.extractor.util_standard import standard_repr, standard_eq
import os.path


class CommandInvocationFeature:
    def __init__(self, cmd_name: str, input_list: List, output_list: List, pkg_list: List, other_list: List,
                 user_list: List, cmd_flag_list=None, cmd_operand_list=None) -> None:
        self.cmd_name: str = cmd_name
        self.input_list: List[str] = input_list
        self.output_list: List[str] = output_list
        self.pkg_list: List[str] = pkg_list
        self.other_list: List[str] = other_list
        self.user_list: List[str] = user_list
        self.cmd_flag_list: Union[List[List[str], List[str]]] = return_empty_list_if_none_else_itself(cmd_flag_list)
        self.cmd_operand_list: Union[List[List[str], List[str]]] = return_empty_list_if_none_else_itself(cmd_operand_list)

    def __repr__(self):
        return standard_repr(self)

    def __eq__(self, other):
        return standard_eq(self, other)

    def set_cmd_info(self, cmd_flag_list: List[str], cmd_operand_list: List[str]):
        self.set_cmd_flag_list(cmd_flag_list)
        self.set_cmd_operand_list(cmd_operand_list)

    def set_cmd_flag_list(self, cmd_flag_list: List[str]):
        self.cmd_flag_list = cmd_flag_list

    def get_cmd_flag_list(self):
        return self.cmd_flag_list

    def set_cmd_operand_list(self, cmd_operand_list: List[str]):
        self.cmd_operand_list = cmd_operand_list

    def get_cmd_operand_list(self):
        return self.cmd_operand_list

    def get_real_input_and_output_path_by_path_pointer(self, pointer: str, attribute_user: str):
        if self.input_list:
            for index in range(len(self.input_list)):
                item = self.get_real_path(self.input_list[index], attribute_user)
                if not os.path.isabs(item):
                    if len(pointer) > 0 and pointer[0] == "$":
                        self.input_list[index] = os.path.normpath(os.path.join(pointer, item))
                    else:
                        self.input_list[index] = os.path.abspath(os.path.join(pointer, item))
                else:
                    self.input_list[index] = item
        if self.output_list:
            for index in range(len(self.output_list)):
                item = self.get_real_path(self.output_list[index], attribute_user)
                if not os.path.isabs(item):
                    if len(pointer) > 0 and pointer[0] == "$":
                        self.output_list[index] = os.path.normpath(os.path.join(pointer, item))
                    else:
                        self.output_list[index] = os.path.abspath(os.path.join(pointer, item))
                else:
                    self.output_list[index] = item

    @staticmethod
    def get_real_path(old_path: str, attribute_user: str) -> str:
        if "~" in old_path:
            if attribute_user == "root":
                return old_path.replace("~", "/root")
            else:
                return old_path.replace("~", f"/home/{attribute_user}")
        return old_path

    def to_dict(self):
        d = dict()
        d['cmd_name'] = self.cmd_name
        d["input_list"] = self.input_list
        d["output_list"] = self.output_list
        d["pkg_list"] = self.pkg_list
        d["output_list"] = self.output_list
        d["user_list"] = self.user_list
        d["cmd_flag_list"] = self.cmd_flag_list
        d["cmd_operand_list"] = self.cmd_operand_list
        return d


# obj1 is the features obtained from raw xargs
def union_xargs_command_feature(obj1: CommandInvocationFeature, obj2: CommandInvocationFeature):
    cmd_name: str = obj2.cmd_name
    input_list: List[str] = obj1.input_list + obj2.input_list
    output_list: List[str] = obj1.output_list + obj2.output_list
    pkg_list: List[str] = obj2.pkg_list
    other_list: List[str] = obj2.pkg_list
    user_list: List[str] = obj2.user_list
    cmd_flag_list: List = [obj1.cmd_flag_list, obj2.cmd_flag_list]
    cmd_operand_list: List = [obj1.cmd_operand_list, obj2.cmd_operand_list]
    feat = CommandInvocationFeature(cmd_name, input_list, output_list, pkg_list, other_list, user_list, cmd_flag_list, cmd_operand_list)
    return feat


def make_pipe_feature(cmd_inv_feature_list: List[CommandInvocationFeature]) -> CommandInvocationFeature:
    command_list: List[str] = []
    input_list: List = []
    output_list: List = []
    pkg_list: List = []
    other_list: List = []
    user_list: List = []
    cmd_flag_list: List = []
    cmd_operand_list: List = []
    for item in cmd_inv_feature_list:
        command_list.append(item.cmd_name)
        input_list.extend(item.input_list)
        output_list.extend(item.output_list)
        pkg_list.extend(item.pkg_list)
        other_list.extend(item.other_list)
        user_list.extend(item.user_list)
        cmd_flag_list.append(item.cmd_flag_list)
        cmd_operand_list.append(item.cmd_operand_list)
    command = ",".join(command_list)
    return CommandInvocationFeature(command, input_list, output_list, pkg_list, other_list, user_list, cmd_flag_list, cmd_operand_list)
