from graphgen.util import standard_eq, return_empty_list_if_none_else_itself
from typing import List, Optional
from .Operand import Operand


class InstructMetaInit:
    def __init__(self, cmd_name: str, operand: Operand, arg_list: List = None,
                 attribute_user: str = "root",
                 attribute_dir: str = "/", eigenvector_init: Optional[List] = None) -> None:
        self.cmd_name: str = cmd_name
        self.operand: Operand = operand
        self.arg_list: list = return_empty_list_if_none_else_itself(arg_list)
        self.attribute_user: str = attribute_user
        self.attribute_dir: str = attribute_dir
        self.eigenvector_init: Optional[List] = eigenvector_init

    def __repr__(self):
        return f'CommandMetaInit({self.cmd_name.__repr__()}, {self.operand.__repr__()}, ' \
               f'{self.arg_list.__repr__()}, {self.attribute_user.__repr__()}, ' \
               f'{self.attribute_dir.__repr__()}, {self.eigenvector_init.__repr__()} ) '

    def __str__(self):
        return f'cmd_name: {self.cmd_name}, {self.operand.__str__()}, ' \
               f'arg_list: {self.arg_list}, attribute_user: {self.attribute_user}, ' \
               f'attribute_dir: {self.attribute_dir}, eigenvector_init: {self.eigenvector_init}'

    def __eq__(self, other) -> bool:
        return standard_eq(self, other)

    def set_operand(self, operand: Operand) -> None:
        self.operand = operand

    def get_operand(self) -> Operand:
        return self.operand

    def set_arg_list(self, arg_list: List) -> None:
        self.arg_list = arg_list

    def get_arg_list(self) -> List:
        return self.arg_list

    def set_eigenvector_init(self, eigenvector_init: List) -> None:
        self.eigenvector_init = eigenvector_init

    def get_eigenvector_init(self) -> Optional[List]:
        return self.eigenvector_init

    def set_attribute_user(self, attribute_user: str) -> None:
        self.attribute_user = attribute_user

    def get_attribute_user(self) -> str:
        return self.attribute_user

    def set_attribute_dir(self, attribute_dir: str) -> None:
        self.attribute_dir = attribute_dir

    def get_attribute_dir(self) -> str:
        return self.attribute_dir
