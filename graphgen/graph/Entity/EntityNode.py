import base64
import hashlib
import re
from abc import abstractmethod, ABCMeta
from typing import Tuple, Dict, List, Set, Optional

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

    @abstractmethod
    def get_entity_create_script(self) -> str:
        pass

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
        return hash(self.to_dict())

    def calc_hash(self):
        hash_object = hashlib.sha256(self.to_dict().encode())
        hex_hash = hash_object.hexdigest()
        alpha_hash = ''.join(filter(str.isalpha, hex_hash))
        if not alpha_hash:
            alpha_hash = 'a' * 64
        return alpha_hash[:64]


class ImageNode(EntityNode):
    NodeName = 'Image'

    def __init__(self, flags: List, value: List) -> None:
        self.name: str = value[0].split(":")[0]
        self.tag: str = value[0].split(":")[1] if value[0].split(":")[1] else "latest"
        self.flags: List = flags
        self.value: List = value

    def pretty(self) -> str:
        original_instruct = "FROM "
        if len(self.flags) != 0:
            original_instruct += " ".join(self.flags) + " "
        original_instruct += " ".join(self.value)
        return original_instruct

    def get_entity_create_script(self) -> str:
        return f''':{self.__class__.NodeName} {self.to_dict()}'''

    def __str__(self) -> str:
        return f"img({self.name}:{self.tag})"


# 可执行命令
class ExecutableNode(EntityNode):
    NodeName = 'ExeCmd'

    def __init__(self, cmd_name: str, cmd_type: str = "general") -> None:
        self.name: str = cmd_name
        self.type: str = cmd_type

    def pretty(self) -> str:
        return ""

    def get_entity_create_script(self) -> str:
        return f''':{self.__class__.NodeName} {self.to_dict()}'''

    def __str__(self) -> str:
        return f"exe_cmd({self.name})"


# RUN
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

    def get_entity_create_script(self) -> str:
        return f''':{self.__class__.NodeName} {self.to_dict()}'''

    def __str__(self) -> str:
        return f"command_node({self.value})"

    def to_tool_pkg_node(self) -> Optional["ToolPkgNode"]:
        url = self.value.split()[-1]
        return ToolPkgNode(url, self.name)


class ToolPkgNode(EntityNode):
    NodeName = 'ToolPkg'

    def __init__(self, url: str, method: str) -> None:
        filename = url.split("/")[-1]
        pattern = re.compile(
            r'^(?P<name>[a-zA-Z0-9]+)'  # 包名，通常包含字母、数字
        )
        # 尝试匹配文件名
        match = pattern.match(filename)
        if match:
            name = match.group('name')
        else:
            name = filename
        self.name: str = name
        self.url: str = url
        self.method: str = method

    def pretty(self) -> str:
        return ""

    def get_entity_create_script(self) -> str:
        return f''':{self.__class__.NodeName} {self.to_dict()}'''

    def __str__(self) -> str:
        return f'tool_package({self.name})'


class SinglePkgNode(EntityNode):
    NodeName = 'Pkg'

    def __init__(self, flags: List, pkg_name: str, version: str, cmd_flag_list: List, cmd_operand_list: List, method: str) -> None:
        self.name: str = pkg_name
        self.version: str = version
        self.flags: List = flags
        self.cmd_flag_list: List = cmd_flag_list
        self.cmd_operand_list: List = [cmd_operand_list[0]] if len(cmd_operand_list) > 1 else cmd_operand_list
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

    def get_entity_create_script(self) -> str:
        return f''':{self.__class__.NodeName} {self.to_dict()}'''

    def __str__(self) -> str:
        return f'package({self.name})'


# apt,pip等的包管理命令
class PkgNode(EntityNode):
    NodeName = 'PkgCmd'

    def __init__(self, flags: List, pkg_cmd: str, cmd_flag_list: List, cmd_operand_list: List, pkg_list: List, version_list: List) -> None:
        self.name: str = pkg_cmd
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
            original_instruct += " ".join(self.cmd_operand_list) + " "
        if len(self.cmd_flag_list) != 0:
            original_instruct += " ".join(self.cmd_flag_list) + " "
        if len(self.pkg_list) > 1:
            for idx, version in enumerate(self.version_list):
                pkg = self.pkg_list[idx]
                if version != "latest":
                    original_instruct += pkg + "==" + version + " "
                else:
                    original_instruct += pkg + " "
        return original_instruct.strip()

    def get_entity_create_script(self) -> str:
        return f''':{self.__class__.NodeName} {self.to_dict()}'''

    def __str__(self) -> str:
        if len(self.pkg_list) == 1:
            return f'package({self.pkg_list[0]})'
        return f'package({self.pkg_list})'

    def split(self) -> List[SinglePkgNode]:
        # 拆分不考虑包名=命令名情况
        return [SinglePkgNode(self.flags, pkg, self.version_list[idx], self.cmd_flag_list, self.cmd_operand_list, self.name) for idx, pkg in
                enumerate(self.pkg_list) if self.name != pkg]


# CMD, ENTRYPOINT
class BootNode(EntityNode):
    NodeName = 'Boot'

    def __init__(self, instruct_name: str, flags: List, value: List) -> None:
        self.name: str = instruct_name
        self.flags: List = flags
        self.value: List = value

    def pretty(self) -> str:
        original_instruct = ""
        original_instruct += self.name + " "
        if len(self.flags) != 0:
            original_instruct += " ".join(self.flags) + " "
        original_instruct += " ".join(self.value)
        return original_instruct

    def get_entity_create_script(self) -> str:
        return f''':{self.__class__.NodeName} {self.to_dict()}'''

    def __str__(self) -> str:
        return f'boot({self.name} {self.value})'


class EnvNode(EntityNode):
    NodeName = 'Env'

    def __init__(self, flags: List, value: Dict) -> None:
        self.name: str = "ENV"
        self.flags: List = flags
        self.var_dict = value

    def pretty(self) -> str:
        original_instruct = "ENV "
        if len(self.flags) != 0:
            original_instruct += " ".join(self.flags) + " "
        for key, value in self.var_dict.items():
            original_instruct += f'{key}="{value}" '
        return original_instruct.strip()

    def get_entity_create_script(self) -> str:
        return f''':{self.__class__.NodeName} {self.to_dict()}'''

    def __str__(self) -> str:
        return f"env({str(self.var_dict)})"


class ArgNode(EntityNode):
    NodeName = 'Arg'

    def __init__(self, flags: List, value: Dict) -> None:
        self.name: str = "ARG"
        self.flags: List = flags
        self.var_dict = value

    def pretty(self) -> str:
        original_instruct = "ARG "
        if len(self.flags) != 0:
            original_instruct += " ".join(self.flags) + " "
        for key, value in self.var_dict.items():
            original_instruct += f'{key}="{value}" '
        return original_instruct.strip()

    def get_entity_create_script(self) -> str:
        return f''':{self.__class__.NodeName} {self.to_dict()}'''

    def __str__(self) -> str:
        return f"arg({str(self.var_dict)})"


class AddOrCopyNode(EntityNode):
    NodeName = 'File'

    def __init__(self, flags: List, value: Dict, types: str) -> None:
        self.name: str = "File"
        self.flags: List = flags
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

    def get_entity_create_script(self) -> str:
        return f''':{self.__class__.NodeName} {self.to_dict()}'''

    def __str__(self) -> str:
        return f'(file):{" ".join(self.flags)} {" ".join(self.src)}'


# 'EXPOSE','VOLUME','USER','WORKDIR','SHELL'
class DefaultNode(EntityNode):
    NodeName = 'OTHER'

    def __init__(self, instruct_name: str, flags: List, value: List) -> None:
        self.name: str = instruct_name
        self.flags: List = flags
        self.value: List = value

    def pretty(self) -> str:
        original_instruct = ""
        original_instruct += self.name + " "
        if len(self.flags) != 0:
            original_instruct += " ".join(self.flags) + " "
        original_instruct += " ".join(self.value)
        return original_instruct

    def get_entity_create_script(self) -> str:
        return f''':{self.__class__.NodeName} {self.to_dict()}'''

    def __str__(self) -> str:
        return f'(other):{self.name} {self.value}'
