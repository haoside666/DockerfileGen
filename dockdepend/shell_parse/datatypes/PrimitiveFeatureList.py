import json

from dockdepend.shell_parse.datatypes.PrimitiveFeature import PrimitiveFeature
from dockdepend.util import standard_repr, standard_eq, return_empty_list_if_none_else_itself
from typing import List, Dict, Union, Tuple
from dockdepend.shell_parse.datatypes.InsturctFeatureInit import InstructFeatureInit
from copy import deepcopy

CMD_TYPE = Union[List[str], List[List[str]]]


class PrimitiveFeatureList:
    def __init__(self, p_feat_list, is_complex: bool = False) -> None:
        self.p_feat_list: List[PrimitiveFeature] = return_empty_list_if_none_else_itself(p_feat_list)
        self.is_complex: bool = is_complex  # 用于标识命令是否复杂，如 def,for,while,if,case都为复杂命令

    def add_var_c_list(self, var_c_list: List[str]):
        if len(var_c_list) == 0:
            return self
        for p_feat in self.p_feat_list:
            for var_c in var_c_list:
                if isinstance(p_feat.command, str):
                    if var_c in p_feat.command:
                        p_feat.var_c_list.append(var_c)
                elif isinstance(p_feat.command, list):
                    if var_c in " | ".join(p_feat.command):
                        p_feat.var_c_list.append(var_c)
        return self

    def set_is_complex_flag(self):
        self.is_complex = True

    def json(self) -> str:
        d = dict()
        d["p_feat_list"] = self.p_feat_list
        return json.dumps(d) + "\n"

    def __repr__(self):
        return standard_repr(self)

    def __eq__(self, other) -> bool:
        return standard_eq(self, other)


def get_pipe_primitive_feature_by_union_primitive_feature_list(items: List[PrimitiveFeatureList]) -> PrimitiveFeatureList:
    var_p_list: List[Tuple[str, str]] = []
    redir_input_list: List[str] = []
    redir_output_list: List[str] = []
    other_list: List[str] = []
    pipe_command: List[str] = []
    is_complex: bool = False

    for item in items:
        for p_feat in item.p_feat_list:
            var_p_list.extend(p_feat.var_p_list)
            pipe_command.append(p_feat.command)
            redir_input_list.extend(p_feat.redir_input_list)
            redir_output_list.extend(p_feat.redir_output_list)
            other_list.extend(p_feat.other_list)
        is_complex = is_complex | item.is_complex
    p_feat = PrimitiveFeature(var_p_list, pipe_command, redir_input_list, redir_output_list, other_list)
    return PrimitiveFeatureList([p_feat], is_complex)


def union_primitive_feature(obj1: PrimitiveFeatureList, obj2: PrimitiveFeatureList) -> PrimitiveFeatureList:
    union_p_feat_list = obj1.p_feat_list + obj2.p_feat_list
    is_complex: bool = obj1.is_complex | obj2.is_complex
    return PrimitiveFeatureList(union_p_feat_list, is_complex)


def union_primitive_feature_list(items: List[PrimitiveFeatureList]) -> PrimitiveFeatureList:
    p_feat_list: List[PrimitiveFeature] = []

    is_complex: bool = False

    for item in items:
        p_feat_list.extend(item.p_feat_list)
        is_complex = is_complex | item.is_complex
    return PrimitiveFeatureList(p_feat_list, is_complex)
