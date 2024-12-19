from graphgen.dockerfile_process.datatypes.ShellFeature import ShellFeature
from graphgen.dockerfile_process.preprocess.datatypes import Operand
from graphgen.dockerfile_process.preprocess.datatypes.InstructMeta import InstructMeta
from graphgen.shell_parse.datatypes.PrimitiveFeature import PrimitiveFeature
from graphgen.util import standard_repr, standard_eq
from graphgen.dockerfile_process.datatypes.InsturctFeature import InstructFeature
from graphgen.dockerfile_process.datatypes.DirectoryTree import DirectoryTree
from typing import Optional, Union, List


class PrimitiveMeta:
    def __init__(self, instruct_meta: InstructMeta) -> None:
        self.cmd_name = instruct_meta.cmd_name
        self.operand = instruct_meta.operand
        self.arg_list = instruct_meta.arg_list
        self.attribute_user = instruct_meta.attribute_user
        self.attribute_dir = instruct_meta.attribute_dir
        self.eigenvector: Union[DirectoryTree, InstructFeature, ShellFeature] = instruct_meta.eigenvector
        self.eigenvector_init = instruct_meta.eigenvector_init
        self.group = 0
        self.is_master = False

    def __repr__(self):
        return f'PrimitiveMeta({self.cmd_name.__repr__()}, {self.operand.__repr__()}, ' \
               f'{self.arg_list.__repr__()}, {self.attribute_user.__repr__()}, ' \
               f'{self.attribute_dir.__repr__()}, {self.eigenvector.__repr__()} ) '

    def __str__(self):
        return f'cmd_name: {self.cmd_name}, {self.operand.__str__()}, ' \
               f'arg_list: {self.arg_list}, attribute_user: {self.attribute_user}, ' \
               f'attribute_dir: {self.attribute_dir}, eigenvector: {self.eigenvector}'

    def __eq__(self, other) -> bool:
        return standard_eq(self, other)

    def pretty(self):
        return self.cmd_name + " " + self.operand.pretty()

    def to_dict(self):
        meta = dict()
        meta["InstructName"] = self.cmd_name
        meta["Operand"] = self.operand.to_json()
        meta["ArgList"] = self.arg_list
        meta["AttributeUser"] = self.attribute_user
        meta["AttributeDir"] = self.attribute_dir
        if self.eigenvector is None:
            meta["Eigenvector"] = "None"
        else:
            meta["Eigenvector"] = self.eigenvector.to_dict()
        return meta

    def set_eigenvector(self, eigenvector: Union[DirectoryTree, ShellFeature]) -> None:
        self.eigenvector = eigenvector

    def get_eigenvector(self) -> Optional[Union[DirectoryTree, ShellFeature]]:
        return self.eigenvector

    def set_operand(self, operand: Operand) -> None:
        self.operand = operand

    def get_operand(self) -> Operand:
        return self.operand

    def set_arg_list(self, arg_list: List) -> None:
        self.arg_list = arg_list

    def get_arg_list(self) -> List:
        return self.arg_list

    def set_eigenvector_init(self, eigenvector_init: Union[List, PrimitiveFeature]) -> None:
        self.eigenvector_init = eigenvector_init

    def get_eigenvector_init(self) -> Optional[Union[List, PrimitiveFeature]]:
        return self.eigenvector_init

    def set_attribute_user(self, attribute_user: str) -> None:
        self.attribute_user = attribute_user

    def get_attribute_user(self) -> str:
        return self.attribute_user

    def set_attribute_dir(self, attribute_dir: str) -> None:
        self.attribute_dir = attribute_dir

    def get_attribute_dir(self) -> str:
        return self.attribute_dir

    def set_is_master(self, is_master: bool) -> None:
        self.is_master = is_master

    def get_is_master(self) -> bool:
        return self.is_master
