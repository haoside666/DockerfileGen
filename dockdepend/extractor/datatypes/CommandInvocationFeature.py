import json
from typing import List
from dockdepend.extractor.util_standard import standard_repr, standard_eq
import os.path


class CommandInvocationFeature:
    def __init__(self, cmd_name: str, input_list: List, output_list: List, pkg_list: List, other_list: List,
                 user_list: List) -> None:
        self.cmd_name: str = cmd_name
        self.input_list: List[str] = input_list
        self.output_list: List[str] = output_list
        self.pkg_list: List[str] = pkg_list
        self.other_list: List[str] = other_list
        self.user_list: List[str] = user_list

    def __repr__(self):
        return standard_repr(self)

    def __eq__(self, other):
        return standard_eq(self, other)

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
        return d


# obj1 is the features obtained from raw xargs
def union_xargs_command_feature(obj1: CommandInvocationFeature, obj2: CommandInvocationFeature):
    cmd_name: str = obj2.cmd_name
    input_list: List[str] = obj1.input_list + obj2.input_list
    output_list: List[str] = obj1.output_list + obj2.output_list
    pkg_list: List[str] = obj2.pkg_list
    other_list: List[str] = obj2.pkg_list
    user_list: List[str] = obj2.user_list
    return CommandInvocationFeature(cmd_name, input_list, output_list, pkg_list, other_list, user_list)
