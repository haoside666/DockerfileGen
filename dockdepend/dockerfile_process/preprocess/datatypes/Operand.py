from dockdepend.util import standard_eq
from typing import Tuple, Optional, Union, Dict, List


# one-line instruction operand entity
class Operand:
    def __init__(self, flags: Tuple, subcmd: Optional[str] = None, value: Union[Tuple, str, Dict] = None,
                 types: str = "default") -> None:
        self.flags = flags
        self.subcmd = subcmd
        self.value = value
        self.type = types

    def __repr__(self):
        return f'Operand({self.flags.__repr__()},{self.subcmd.__repr__()},{self.value.__repr__()},{self.type.__repr__()})'

    def __str__(self):
        return f'flags: {self.flags}, subcmd: {self.subcmd}, value: {self.value}, type: {self.type}'

    def to_json(self):
        json_data = dict()
        json_data["flags"] = self.flags
        if self.subcmd is None:
            json_data["subcmd"] = "None"
        else:
            json_data["subcmd"] = self.subcmd
        json_data["value"] = self.value
        json_data["type"] = self.type
        return json_data

    # 得到原始指令
    def pretty(self) -> str:
        original_instruct = ""
        if len(self.flags) != 0:
            original_instruct += " ".join(self.flags) + " "
        if self.subcmd is not None:
            original_instruct += self.subcmd + " "
        if isinstance(self.value, Tuple):
            original_instruct += " ".join(self.value)
        elif isinstance(self.value, str):
            original_instruct += self.value
        elif isinstance(self.value, Dict):
            value = self.value
            if "src_dir" in value and isinstance(value["src_dir"], Tuple):
                src_dir = self.value["src_dir"]
                dst_dir = self.value["dst_dir"]
                result = " ".join(src_dir) + " " + dst_dir
            else:
                items = []
                for k, v in value.items():
                    if v == "":
                        items.append(f'{k}=""')
                    else:
                        items.append(f'{k}={v}')
                result = " ".join(items)
            original_instruct += result
        return original_instruct

    def __eq__(self, other) -> bool:
        return standard_eq(self, other)

    def set_type(self, types) -> None:
        self.type = types

    def set_subcmd(self, subcmd) -> None:
        self.subcmd = subcmd

    def set_value(self, value) -> None:
        self.value = value

    def if_value_is_dict_to_get_dict(self) -> Dict:
        assert isinstance(self.value, Dict)
        return self.value

    def if_value_is_dict_to_get_keys(self) -> List:
        assert isinstance(self.value, Dict)
        return list(self.value.keys())

    def if_value_is_dir_dict_to_get_src_dir(self) -> Tuple:
        assert isinstance(self.value, Dict)
        return self.value["src_dir"]

    def if_value_is_dir_dict_to_get_dst_dir(self) -> str:
        assert isinstance(self.value, Dict)
        return self.value["dst_dir"]
