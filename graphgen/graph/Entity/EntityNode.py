import base64
import hashlib
import os
import re
import time
from abc import abstractmethod, ABCMeta
from copy import deepcopy
from typing import Tuple, Dict, List, Set, Optional, Union

from graphgen.config.definitions import TOOL_PKG_METHOD
from graphgen.graph.Entity.cache import ENTITY_INFO_DICT, get_entity_to_dict_info_by_obj_id, set_entity_to_dict_info_by_obj_id
from graphgen.util import standard_repr, standard_eq


class EntityNode(metaclass=ABCMeta):
    NodeName = 'None'

    @abstractmethod
    def __init__(self, name: str) -> None:
        self.name = name

    @abstractmethod
    def pretty(self) -> str:
        """
        Returns to the original dockerfile command line.
        """
        pass

    def get_entity_create_script(self) -> str:
        return f''':{self.__class__.NodeName} {self.to_dict()}'''

    def __repr__(self):
        return standard_repr(self)

    def __eq__(self, other) -> bool:
        return standard_eq(self, other)

    def to_dict(self) -> str:
        content = "{"
        lis = []
        for key, value in self.__dict__.items():
            if isinstance(value, list):
                lis.append(f"{key}: {value}")
            else:
                lis.append(f"{key}: '{value}'")
        content += ", ".join(lis) + "}"
        return content

    def __hash__(self) -> int:
        m_addr = id(self)
        if m_addr in ENTITY_INFO_DICT:
            return hash(get_entity_to_dict_info_by_obj_id(m_addr))
        else:
            value = self.get_flag_str()
            set_entity_to_dict_info_by_obj_id(m_addr, value)
            return hash(value)

    def calc_hash(self):
        m_addr = id(self)
        if m_addr in ENTITY_INFO_DICT:
            value = get_entity_to_dict_info_by_obj_id(m_addr)
        else:
            value = self.get_flag_str()
            set_entity_to_dict_info_by_obj_id(m_addr, value)
        hash_object = hashlib.sha256(value.encode())
        base_hash = hash_object.hexdigest()
        return self.NodeName.lower() + base_hash[:128]

    @abstractmethod
    def get_flag_str(self) -> str:
        return ""


class ImageNode(EntityNode):
    NodeName = 'Image'

    def __init__(self, flags: List, value: List) -> None:
        if "@sha256" not in value[0]:
            if ":" not in value[0]:
                self.name: str = value[0]
                self.tag: str = "latest"
            else:
                self.name: str = value[0].split(":")[0].strip()
                self.tag: str = value[0].split(":")[1].strip()
        else:
            self.name: str = value[0].split("@")[0]
            self.tag: str = value[0].split("@")[1] if value[0].split("@")[1] else "latest"
        self.flags: List = flags
        self.value: List = value[:1]

    def pretty(self) -> str:
        original_instruct = "FROM "
        if len(self.flags) != 0:
            original_instruct += " ".join(self.flags) + " "
        original_instruct += " ".join(self.value)
        return original_instruct

    def __str__(self) -> str:
        return f"img({self.name}:{self.tag})"

    def get_flag_str(self) -> str:
        return f"{self.name}:{self.tag}"


# 可执行命令
class ExecutableNode(EntityNode):
    NodeName = 'ExeCmd'

    def __init__(self, name: str, cmd_type: str = "general") -> None:
        self.name: str = name
        self.type: str = cmd_type

    def pretty(self) -> str:
        return ""

    def __str__(self) -> str:
        return f"exe_cmd({self.name})"

    def get_flag_str(self) -> str:
        return f"{self.name} {self.type}"


class CommandNode(EntityNode):
    NodeName = 'Cmd'

    def __init__(self, cmd_list: List, flags: List, value: str, cmd_type: str) -> None:
        self.name: str = ",".join(cmd_list)
        self.cmd_list: List = cmd_list
        self.flags: List = flags
        self.value: str = value
        self.cmd_type: str = cmd_type

    def pretty(self) -> str:
        original_instruct = "RUN "
        if len(self.flags) != 0:
            original_instruct += " ".join(self.flags) + " "
        original_instruct += self.value
        return original_instruct

    def __str__(self) -> str:
        return f"command_node({self.value})"

    def get_flag_str(self) -> str:
        return self.value

    def to_tool_pkg_node(self) -> Optional["ToolPkgNode"]:
        # 匹配以https://开头或http://git@开头url
        pattern = r'((https?:\/\/)|(git@))+[^\s]+'
        match = re.search(pattern, self.value)
        if not match:
            raise Exception("ERROR: cmd_type of the command node is not 'url'")
        else:
            url = match.group()
        return ToolPkgNode(url, self.name)


class ToolPkgNode(EntityNode):
    NodeName = 'ToolPkg'

    def __init__(self, url: str, method: str, cmd_list: List = None) -> None:
        union_set = set(method.split(",")) & TOOL_PKG_METHOD
        if len(union_set) >= 1:
            method = list(union_set)[0]
        else:
            raise Exception("ERROR: method of the tool package node is not supported")
        self.name: str = self.extract_dir_name(url, method)
        self.url: str = url
        self.method: str = method
        self.cmd_list: List = cmd_list if cmd_list else []

    def pretty(self) -> str:
        return ""

    def __str__(self) -> str:
        return f'tool_package({self.name})'

    def get_flag_str(self) -> str:
        return f'{self.url} {self.cmd_list}'

    @staticmethod
    def extract_dir_name(url: str, method: str):
        if method == "git":
            name = os.path.basename(url)
            index = name.find(".git")
            if index != -1:
                return name[:index]
            else:
                t = name.rpartition(".")
                if t[0] == "":
                    return name
                else:
                    return t[0]
        else:
            return url.rpartition("/")[-1]

    def set_cmd_list(self, cmd_list):
        self.cmd_list = cmd_list


class SinglePkgNode(EntityNode):
    NodeName = 'Pkg'

    def __init__(self, name: str, version: str, flags: List, cmd_flag_list: List, cmd_operand_list: List, method: str) -> None:
        self.name: str = name
        self.version: str = version
        self.flags: List = flags
        self.cmd_flag_list: List = cmd_flag_list
        self.cmd_operand_list: List = cmd_operand_list
        self.method: str = method

    def pretty(self) -> str:
        original_instruct = "RUN "
        if len(self.flags) != 0:
            original_instruct += " ".join(self.flags) + " "
        original_instruct += self.method + " "
        if len(self.cmd_operand_list) != 0:
            original_instruct += " ".join(self.cmd_operand_list) + " "
        if len(self.cmd_flag_list) != 0:
            original_instruct += " ".join(self.cmd_flag_list) + " "
        if self.version != "latest":
            original_instruct += self.name
        else:
            original_instruct += self.name + "==" + self.version
        return original_instruct

    def __str__(self) -> str:
        return f'package({self.name})'

    def get_flag_str(self) -> str:
        content = "{"
        lis = []
        for key, value in self.__dict__.items():
            if isinstance(value, list):
                lis.append(f"{key}: {value}")
            else:
                lis.append(f"{key}: '{value}'")
        content += ", ".join(lis) + "}"
        return content


# apt,pip等的包管理命令
class PkgNode(EntityNode):
    NodeName = 'PkgCmd'

    def __init__(self, name: str, flags: List, cmd_flag_list: List, cmd_operand_list: List, pkg_list: List, version_list: List) -> None:
        self.name: str = name
        self.flags: List = flags
        self.cmd_flag_list: List = cmd_flag_list
        self.cmd_operand_list: List = cmd_operand_list
        self.pkg_list: List = pkg_list
        self.version_list: List = version_list

    def pretty(self) -> str:
        original_instruct = "RUN "
        if len(self.flags) != 0:
            original_instruct += " ".join(self.flags) + " "
        original_instruct += self.name + " "
        if len(self.cmd_operand_list) != 0:
            original_instruct += self.cmd_operand_list[0] + " "
        if len(self.cmd_flag_list) != 0:
            original_instruct += " ".join(self.cmd_flag_list) + " "
        if len(self.cmd_operand_list) > 1:
            original_instruct += " ".join(self.cmd_operand_list[1:]) + " "
        # if len(self.pkg_list) > 1:
        #     for idx, version in enumerate(self.version_list):
        #         pkg = self.pkg_list[idx]
        #         if version != "latest":
        #             original_instruct += pkg + "==" + version + " "
        #         else:
        #             original_instruct += pkg + " "
        return original_instruct.strip()

    def __str__(self) -> str:
        if len(self.pkg_list) == 1:
            return f'package({self.pkg_list[0]})'
        return f'package({self.pkg_list})'

    def get_flag_str(self) -> str:
        real_dict = deepcopy(self.__dict__)
        real_dict.pop("pkg_list")
        real_dict.pop("version_list")
        content = "{"
        lis = []
        for key, value in real_dict.items():
            if isinstance(value, list):
                lis.append(f"{key}: {value}")
            else:
                lis.append(f"{key}: '{value}'")
        content += ", ".join(lis) + "}"
        return content

    def split(self) -> List[SinglePkgNode]:
        # # 拆分不考虑包名=命令名情况
        # return [SinglePkgNode(self.flags, pkg, self.version_list[idx], self.cmd_flag_list, self.cmd_operand_list, self.name) for idx, pkg in
        #         enumerate(self.pkg_list) if self.name != pkg]
        return [SinglePkgNode(pkg, self.version_list[idx], self.flags, self.cmd_flag_list, [self.cmd_operand_list[0]], self.name) for idx, pkg in
                enumerate(self.pkg_list)]


# CMD, ENTRYPOINT
class BootNode(EntityNode):
    NodeName = 'Boot'

    def __init__(self, name: str, flags: List, value: List) -> None:
        self.name: str = name
        self.flags: List = flags
        self.value: List = value

    def pretty(self) -> str:
        original_instruct = ""
        original_instruct += self.name + " "
        if len(self.flags) != 0:
            original_instruct += " ".join(self.flags) + " "
        original_instruct += " ".join(self.value)
        return original_instruct

    def __str__(self) -> str:
        return f'boot({self.name} {self.value})'

    def get_flag_str(self) -> str:
        return f"{self.name} {self.flags} {self.value}"


class EnvNode(EntityNode):
    NodeName = 'Env'

    def __init__(self, flags: List, value: List) -> None:
        self.name: str = "ENV"
        self.flags: List = flags
        self.value: List = value

    def pretty(self) -> str:
        original_instruct = "ENV "
        if len(self.flags) != 0:
            original_instruct += " ".join(self.flags) + " "
        for item in self.value:
            original_instruct += f'{item} '
        return original_instruct.strip()

    def __str__(self) -> str:
        return f"env({str(self.value)})"

    def get_flag_str(self) -> str:
        return f"{self.value}"


class ArgNode(EntityNode):
    NodeName = 'Arg'

    def __init__(self, flags: List, value: List) -> None:
        self.name: str = "ARG"
        self.flags: List = flags
        self.value: List = value

    def pretty(self) -> str:
        original_instruct = "ARG "
        if len(self.flags) != 0:
            original_instruct += " ".join(self.flags) + " "
        for item in self.value:
            original_instruct += f'{item} '
        return original_instruct.strip()

    def __str__(self) -> str:
        return f"arg({str(self.value)})"

    def get_flag_str(self) -> str:
        return f"{self.value}"


class AddOrCopyNode(EntityNode):
    NodeName = 'File'

    def __init__(self, flags: List, src: List, dest: str, types: str) -> None:
        self.name: str = "File"
        self.flags: List = flags
        self.src: List = src
        self.dest: str = dest
        self.types: str = types

    def pretty(self) -> str:
        original_instruct = ""
        if self.types == "special":
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

    def __str__(self) -> str:
        return f'(file):{" ".join(self.flags)} {" ".join(self.src)} {self.dest}'

    def get_flag_str(self) -> str:
        return f'{self.name} {self.src} {self.dest}'


# 'EXPOSE','VOLUME','USER','WORKDIR','SHELL'
class DefaultNode(EntityNode):
    NodeName = 'OTHER'

    def __init__(self, name: str, flags: List, value: List) -> None:
        self.name: str = name
        self.flags: List = flags
        self.value: List = value

    def pretty(self) -> str:
        original_instruct = ""
        original_instruct += self.name + " "
        if len(self.flags) != 0:
            original_instruct += " ".join(self.flags) + " "
        original_instruct += " ".join(self.value)
        return original_instruct

    def __str__(self) -> str:
        return f'(other):{self.name} {self.value}'

    def get_flag_str(self) -> str:
        return f"{self.name} {self.value}"


def gen_entity_node_by_label_and_property(label: str, property_dict: Dict) -> EntityNode:
    if label == "Cmd":
        return CommandNode(property_dict["cmd_list"], property_dict["flags"], property_dict["value"], property_dict["cmd_type"])
    elif label == "PkgCmd":
        return PkgNode(property_dict["name"], property_dict["flags"], property_dict["cmd_flag_list"],
                       property_dict["cmd_operand_list"], property_dict["pkg_list"], property_dict["version_list"])
    elif label == "File":
        return AddOrCopyNode(property_dict["flags"], property_dict["src"], property_dict["dest"], property_dict["types"])
    elif label == "Env":
        return EnvNode(property_dict["flags"], property_dict["value"])
    elif label == "Other":
        return DefaultNode(property_dict["name"], property_dict["flags"], property_dict["value"])
    elif label == "ToolPkg":
        return ToolPkgNode(property_dict["url"], property_dict["method"], property_dict["cmd_list"])
    elif label == "Arg":
        return ArgNode(property_dict["flags"], property_dict["value"])
    elif label == "Boot":
        return BootNode(property_dict["name"], property_dict["flags"], property_dict["value"])
    raise Exception("Unknown entity node type: " + label)
