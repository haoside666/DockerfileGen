from abc import abstractmethod, ABCMeta
from typing import Tuple, Dict, List

from dockdepend.util import standard_repr, standard_eq


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

    def __init__(self, flags: Tuple, value: str) -> None:
        self.flags: Tuple = flags
        self.value: str = value

    def pretty(self) -> str:
        original_instruct = "RUN "
        if len(self.flags) != 0:
            original_instruct += " ".join(self.flags) + " "
        original_instruct += self.value
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
