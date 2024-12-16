import json

from dockdepend.util import standard_repr, standard_eq, return_empty_list_if_none_else_itself
from typing import List, Dict, Union, Tuple
from dockdepend.shell_parse.datatypes.InsturctFeatureInit import InstructFeatureInit
from copy import deepcopy

CMD_TYPE = Union[List[str], List[List[str]]]


class CommandFeature:
    def __init__(self, var_p_list: List[Tuple[str, str]] = None, command_list: CMD_TYPE = None,
                 redir_input_list: List[str] = None, redir_output_list: List[str] = None,
                 other_list: List[str] = None, is_complex: bool = False) -> None:
        self.var_p_list: List[Tuple[str, str]] = return_empty_list_if_none_else_itself(var_p_list)
        self.command_list: CMD_TYPE = return_empty_list_if_none_else_itself(command_list)
        self.redir_input_list: List[str] = return_empty_list_if_none_else_itself(redir_input_list)
        self.redir_output_list: List[str] = return_empty_list_if_none_else_itself(redir_output_list)
        self.other_list: List[str] = return_empty_list_if_none_else_itself(other_list)
        self.is_complex: bool = is_complex  # 用于标识命令是否复杂，如 def,for,while,if,case都为复杂命令

    def to_instruct_feature_init(self) -> InstructFeatureInit:
        pass

    def add_redir_list_to_feature(self, redir_input_list: List[str], redir_output_list: List[str],
                                  other_list: List[str]):
        self.redir_input_list.extend(redir_input_list)
        self.redir_output_list.extend(redir_output_list)
        self.other_list.extend(other_list)

    def add_other_list_to_feature(self, other_list: List[str]):
        self.other_list.extend(other_list)

    def set_is_complex_flag(self):
        self.is_complex = True

    def transform_command_list_to_other_list(self):
        self.other_list.extend(deepcopy(self.command_list))
        self.command_list.clear()

    def json(self) -> str:
        d = dict()
        d["var_p_list"] = self.var_p_list
        d["command_list"] = self.command_list
        d["redir_input_list"] = self.redir_input_list
        d["redir_output_list"] = self.redir_output_list
        d["other_list"] = self.other_list
        return json.dumps(d) + "\n"

    def get_instruct_feature_init_add_var_c_list(self, var_c_list: List[str]) -> InstructFeatureInit:
        return InstructFeatureInit(self.var_p_list, self.command_list, self.redir_input_list,
                                   self.redir_output_list, var_c_list, self.other_list)

    def is_empty(self):
        return len(self.var_p_list) == 0 and len(self.command_list) == 0 and len(self.redir_input_list) == 0 and \
               len(self.redir_output_list) == 0 and len(self.other_list) == 0

    def __repr__(self):
        return standard_repr(self)

    def __eq__(self, other) -> bool:
        return standard_eq(self, other)


def union_command_feature(obj1: CommandFeature, obj2: CommandFeature) -> CommandFeature:
    var_p_list: List[Tuple[str, str]] = obj1.var_p_list + obj2.var_p_list
    command_list: CMD_TYPE = obj1.command_list + obj2.command_list
    redir_input_list: List[str] = obj1.redir_input_list + obj2.redir_input_list
    redir_output_list: List[str] = obj1.redir_output_list + obj2.redir_output_list
    other_list: List[str] = obj1.other_list + obj2.other_list
    is_complex: bool = obj1.is_complex | obj2.is_complex
    return CommandFeature(var_p_list, command_list, redir_input_list, redir_output_list, other_list, is_complex)


def get_pipe_command_feature_by_union_command_feature_list(items: List[CommandFeature]) -> CommandFeature:
    var_p_list: List[Tuple[str, str]] = []
    command_list: List[str] = []
    redir_input_list: List[str] = []
    redir_output_list: List[str] = []
    other_list: List[str] = []
    pipe_list: List[List[str]] = []
    is_complex: bool = False
    for item in items:
        var_p_list.extend(item.var_p_list)
        for cmd in item.command_list:
            if isinstance(cmd, str):
                command_list.append(cmd)
            elif isinstance(cmd, list):
                pipe_list.append(cmd)
        redir_input_list.extend(item.redir_input_list)
        redir_output_list.extend(item.redir_output_list)
        other_list.extend(item.other_list)
        is_complex = is_complex | item.is_complex
    if command_list:
        pipe_list.append(command_list)
    return CommandFeature(var_p_list, pipe_list, redir_input_list, redir_output_list, other_list, is_complex)


def get_command_feature_by_union_command_feature_list(items: List[CommandFeature]) -> CommandFeature:
    var_p_list: List[Tuple[str, str]] = []
    command_list: CMD_TYPE = []
    redir_input_list: List[str] = []
    redir_output_list: List[str] = []
    other_list: List[str] = []
    is_complex: bool = False

    for item in items:
        var_p_list.extend(item.var_p_list)
        command_list.extend(item.command_list)
        redir_input_list.extend(item.redir_input_list)
        redir_output_list.extend(item.redir_output_list)
        other_list.extend(item.other_list)
        is_complex = is_complex | item.is_complex
    return CommandFeature(var_p_list, command_list, redir_input_list, redir_output_list, other_list, is_complex)


def read_jsons(file_path) -> CommandFeature:
    with open(file_path, "r") as file:
        feat_list: List[CommandFeature] = []
        for line in file:
            d: Dict = json.loads(line)
            var_p_list = d["var_p_list"]
            command_list = d["command_list"]
            redir_input_list = d["redir_input_list"]
            redir_output_list = d["redir_output_list"]
            other_list = d["other_list"]
            feat = CommandFeature(var_p_list, command_list, redir_input_list, redir_output_list, other_list)
            feat_list.append(feat)
        return get_command_feature_by_union_command_feature_list(feat_list)
