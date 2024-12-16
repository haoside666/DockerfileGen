from dockdepend.util import standard_eq
from typing import Optional, Union
from .InstructMetaInit import InstructMetaInit
from dockdepend.dockerfile_process.datatypes.InsturctFeature import InstructFeature
from dockdepend.dockerfile_process.datatypes.DirectoryTree import DirectoryTree
from copy import deepcopy


# The meta-information entity corresponding to a line of instructions
# arg_list: for env and arg instructions
# attribute_user: for user instruction
# attribute_dir: used to indicate the path of the current instruction
# eigenvector: for special instruction
class InstructMeta(InstructMetaInit):
    def __init__(self, cmd_meta_init: InstructMetaInit,
                 eigenvector: Optional[Union[DirectoryTree, InstructFeature]] = None) -> None:
        cmd_name = cmd_meta_init.cmd_name
        operand = deepcopy(cmd_meta_init.operand)
        arg_list = deepcopy(cmd_meta_init.arg_list)
        attribute_user = cmd_meta_init.attribute_user
        attribute_dir = cmd_meta_init.attribute_dir
        eigenvector_init = deepcopy(cmd_meta_init.eigenvector_init)
        super().__init__(cmd_name, operand, arg_list, attribute_user, attribute_dir, eigenvector_init)
        self.eigenvector = eigenvector

    def __repr__(self):
        return f'CommandMeta({self.cmd_name.__repr__()}, {self.operand.__repr__()}, ' \
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

    def set_eigenvector(self, eigenvector: Union[DirectoryTree, InstructFeature]) -> None:
        self.eigenvector = eigenvector

    def get_eigenvector(self) -> Optional[Union[DirectoryTree, InstructFeature]]:
        return self.eigenvector
