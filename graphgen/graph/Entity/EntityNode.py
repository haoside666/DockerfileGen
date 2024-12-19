from abc import abstractmethod, ABCMeta
from typing import Tuple, Dict, List, Set

from graphgen.util import standard_repr, standard_eq


class EntityNode(metaclass=ABCMeta):
    NodeName = 'None'

    @abstractmethod
    def pretty(self) -> str:
        """
        Returns to the original dockerfile command line.
        """
        pass

    def __repr__(self):
        return standard_repr(self)

    def __eq__(self, other) -> bool:
        return standard_eq(self, other)


class ImageNode(EntityNode):
    NodeName = 'Image'

    def __init__(self, flags: Tuple, value: Tuple) -> None:
        self.image_name = value[0].split(":")[0]
        self.tag = value[0].split(":")[1] if value[0].split(":")[1] else "latest"
        self.flags: Tuple = flags
        self.value: Tuple = value

    def pretty(self) -> str:
        original_instruct = "FROM "
        if len(self.flags) != 0:
            original_instruct += " ".join(self.flags) + " "
        original_instruct += " ".join(self.value)
        return original_instruct


# RUN
class CommandNode(EntityNode):
    NodeName = 'Cmd'

    def __init__(self, cmd_set: Set, flags: Tuple, value: str, cmd_type: str) -> None:
        self.cmd_set: Set = cmd_set
        self.flags: Tuple = flags
        self.value: str = value
        self.cmd_type: str = cmd_type

    def pretty(self) -> str:
        original_instruct = "RUN "
        if len(self.flags) != 0:
            original_instruct += " ".join(self.flags) + " "
        original_instruct += self.value
        return original_instruct


# apt,pip等的包管理命令
class PkgNode(EntityNode):
    NodeName = 'Pkg'

    def __init__(self, flags: Tuple, pkg_cmd: str, cmd_flag_list: List, cmd_operand_list: List, pkg_set: Set) -> None:
        self.flags: Tuple = flags
        self.pkg_cmd: str = pkg_cmd
        self.cmd_flag_list: List = cmd_flag_list
        self.cmd_operand_list: List = cmd_operand_list
        self.pkg_set: Set = pkg_set

    def pretty(self) -> str:
        original_instruct = "RUN "
        if len(self.flags) != 0:
            original_instruct += " ".join(self.flags) + " "
        original_instruct += self.pkg_cmd + " "
        if len(self.cmd_operand_list) != 0:
            original_instruct += self.cmd_operand_list[0] + " "
        if len(self.cmd_flag_list) != 0:
            original_instruct += " ".join(self.cmd_flag_list) + " "
        if len(self.cmd_operand_list) > 1:
            original_instruct += " ".join(self.cmd_operand_list[1:]) + " "
        return original_instruct


# CMD, ENTRYPOINT
class BootNode(EntityNode):
    NodeName = 'Boot'

    def __init__(self, instruct_name: str, flags: Tuple, value: Tuple) -> None:
        self.instruct_name: str = instruct_name
        self.flags: Tuple = flags
        self.value: Tuple = value

    def pretty(self) -> str:
        original_instruct = ""
        original_instruct += self.instruct_name + " "
        if len(self.flags) != 0:
            original_instruct += " ".join(self.flags) + " "
        original_instruct += " ".join(self.value)
        return original_instruct


class EnvNode(EntityNode):
    NodeName = 'Env'

    def __init__(self, flags: Tuple, value: Dict) -> None:
        self.flags: Tuple = flags
        self.var_dict = value

    def pretty(self) -> str:
        original_instruct = "ENV "
        if len(self.flags) != 0:
            original_instruct += " ".join(self.flags) + " "
        for key, value in self.var_dict.items():
            original_instruct += f'{key}="{value}" '
        return original_instruct.strip()


class ArgNode(EntityNode):
    NodeName = 'Arg'

    def __init__(self, flags: Tuple, value: Dict) -> None:
        self.flags: Tuple = flags
        self.var_dict = value

    def pretty(self) -> str:
        original_instruct = "ARG "
        if len(self.flags) != 0:
            original_instruct += " ".join(self.flags) + " "
        for key, value in self.var_dict.items():
            original_instruct += f'{key}="{value}" '
        return original_instruct.strip()


class AddOrCopyNode(EntityNode):
    NodeName = 'File'

    def __init__(self, flags: Tuple, value: Dict, types: str) -> None:
        self.flags: Tuple = flags
        self.src: List = value["src_dir"]
        self.dest: str = value["dst_dir"]
        self.type: str = types

    def pretty(self) -> str:
        original_instruct = ""
        if self.type == "special":
            original_instruct += "ADD "
        else:
            original_instruct += "COPY "
        if len(self.flags) != 0:
            original_instruct += " ".join(self.flags) + " "
        if len(self.src) != 0:
            original_instruct += " ".join(self.src) + " "
        if len(self.dest) != 0:
            original_instruct += self.dest
        return original_instruct


# 'EXPOSE','VOLUME','USER','WORKDIR','SHELL'
class DefaultNode(EntityNode):
    NodeName = 'OTHER'

    def __init__(self, instruct_name: str, flags: Tuple, value: Tuple) -> None:
        self.instruct_name: str = instruct_name
        self.flags: Tuple = flags
        self.value: Tuple = value

    def pretty(self) -> str:
        original_instruct = ""
        original_instruct += self.instruct_name + " "
        if len(self.flags) != 0:
            original_instruct += " ".join(self.flags) + " "
        original_instruct += " ".join(self.value)
        return original_instruct
