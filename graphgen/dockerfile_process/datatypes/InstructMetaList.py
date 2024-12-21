import json
import os.path
import re
import sys

from graphgen.util import standard_eq
from typing import List, Dict, Set
from graphgen.config.definitions import NOT_CHANGE_DIRECTIVES
from graphgen.dockerfile_process.preprocess.datatypes.InstructMetaInit import InstructMetaInit
from graphgen.dockerfile_process.preprocess.datatypes.InstructMeta import InstructMeta
from graphgen.dockerfile_process.datatypes.DirectoryTree import DirectoryTree
from graphgen.dockerfile_process.datatypes.InstructFeature import InstructFeature
from graphgen.shell_parse.parse import parse_shell_cmd_to_instruct_feature
from graphgen.shell_parse.datatypes import InsturctFeatureInit
from graphgen.exception.CustomizedException import ParsingException
from graphgen.extractor.extractor_cli import get_command_list_feature


# a meta-information entity corresponding to a build phase
class InstructMetaList:
    def __init__(self, build_ctx: str, cmd_meta_init_list: List[InstructMetaInit] = None) -> None:
        self.build_ctx: str = build_ctx
        cmd_meta_list: List[InstructMeta] = [InstructMeta(item) for item in cmd_meta_init_list]
        self.arg_dict: Dict = {}
        self.cmd_meta_list: List[InstructMeta] = self.get_command_meta_list(cmd_meta_list)

    def __repr__(self):
        repr_str = f'{self.__class__}'
        if len(self.__dict__) != 0:
            repr_str += f': \n'
        else:
            repr_str += f'\n'
        repr_str += f'cmd_meta_list: \n'
        for item in self.cmd_meta_list:
            repr_str += f'\t {item.__repr__()}\n'
        repr_str += f'arg_dict: \n'
        repr_str += f'\t {self.arg_dict.__repr__()}\n'
        return repr_str

    def __str__(self):
        repr_str = f'{self.__class__}'
        if len(self.__dict__) != 0:
            repr_str += f': \n'
        else:
            repr_str += f'\n'
        repr_str += f'cmd_meta_list: \n'
        for item in self.cmd_meta_list:
            repr_str += f'\t {item.__str__()}\n'
        repr_str += f'arg_dict: \n'
        repr_str += f'\t {self.arg_dict.__str__()}\n'
        return repr_str

    def __eq__(self, other) -> bool:
        return standard_eq(self, other)

    def length(self) -> int:
        return len(self.cmd_meta_list)

    def get_command_meta_list(self, cmd_meta_list: List[InstructMeta]) -> List[InstructMeta]:
        self.get_arg_dict_by_fulled_command_meta_list(cmd_meta_list)
        self.set_null_value_in_the_dictionary_to_original_form()
        self.__get_real_command_meta_list_by_arg_dict(cmd_meta_list)
        # self.__mark_attribute_dir_and_user(cmd_meta_list)
        return cmd_meta_list

    # Get a dictionary of arg in the build phase
    def get_arg_dict_by_fulled_command_meta_list(self, cmd_meta_list: List[InstructMeta]) -> None:
        self.arg_dict = {}
        for command_meta in cmd_meta_list:
            if command_meta.cmd_name in {"ARG", "ENV"}:
                if command_meta.arg_list:
                    command_meta.arg_list = self.strip_without_arg_in_refer_list(command_meta.arg_list,
                                                                                 set(self.arg_dict.keys()))
                    if command_meta.arg_list:
                        dict1 = command_meta.get_operand().if_value_is_dict_to_get_dict()
                        self.arg_dict.update(self.__strip_known_arg_list_in_dict(dict1, command_meta.arg_list))
                    else:
                        dict1 = command_meta.get_operand().if_value_is_dict_to_get_dict()
                        self.arg_dict.update(dict1)
                else:
                    self.arg_dict.update(command_meta.get_operand().if_value_is_dict_to_get_dict())

    def set_null_value_in_the_dictionary_to_original_form(self):
        for k, v in self.arg_dict.items():
            if v == "":
                self.arg_dict[k] = "${" + k + "}"

    def __get_real_command_meta_list_by_arg_dict(self, cmd_meta_list: List[InstructMeta]) -> None:
        for cmd_meta in cmd_meta_list:
            if len(cmd_meta.arg_list) != 0:
                if cmd_meta.cmd_name == "RUN":
                    self.__get_run_from_real_value(cmd_meta)
                elif cmd_meta.cmd_name in {"ARG", "ENV", "COPY", "ADD"}:
                    self.__get_dict_from_real_value(cmd_meta)
                else:
                    self.__get_tuple_from_real_value(cmd_meta)

    def __get_run_from_real_value(self, cmd_meta: InstructMeta) -> None:
        cmd_meta.arg_list = self.strip_without_arg_in_refer_list(cmd_meta.arg_list, set(self.arg_dict.keys()))
        value = cmd_meta.get_operand().value
        cmd_meta.get_operand().set_value(self.__strip_known_arg_list_in_string(value, cmd_meta.arg_list))

    def __get_tuple_from_real_value(self, cmd_meta: InstructMeta) -> None:
        cmd_meta.arg_list = self.strip_without_arg_in_refer_list(cmd_meta.arg_list, set(self.arg_dict.keys()))
        t = cmd_meta.get_operand().value
        real_t = []
        for value in t:
            if '$' in value:
                value = self.__strip_known_arg_list_in_string(value, cmd_meta.arg_list)
            real_t.append(value)
        cmd_meta.get_operand().set_value(tuple(real_t))

    def __get_dict_from_real_value(self, cmd_meta: InstructMeta) -> None:
        arg_list = cmd_meta.arg_list
        dict1 = cmd_meta.get_operand().value
        cmd_meta.get_operand().set_value(self.__strip_known_arg_list_in_dict(dict1, arg_list))

    def __strip_known_arg_list_in_string(self, s: str, arg_list: List) -> str:
        s = self.strip_parentheses(s, arg_list)
        for arg in arg_list:
            if arg in self.arg_dict:
                s = s.replace(f'${arg}', self.arg_dict[arg])
        return s

    def __strip_known_arg_list_in_dict(self, dict1: Dict, arg_list: List) -> Dict:
        s = json.dumps(dict1)
        s = self.strip_parentheses(s, arg_list)
        try:
            for arg in arg_list:
                if arg in self.arg_dict:
                    s = s.replace(f'${arg}', self.arg_dict[arg])
            dict2: Dict = json.loads(s)
            return dict2
        # a problem with env variable substitution in the window system image
        except json.decoder.JSONDecodeError:
            s = re.sub(r'(?<!\\)\\(?!\\)', r'\\\\', s)
            dict2: Dict = json.loads(s)
            return dict2

    def __mark_attribute_dir_and_user(self, cmd_meta_list: List[InstructMeta]) -> None:
        current_user = "root"
        current_dir = "/"
        for cmd_meta in cmd_meta_list:
            cmd_name = cmd_meta.cmd_name
            if cmd_name in NOT_CHANGE_DIRECTIVES:
                pass
            # Dict
            elif cmd_name == "ADD" or cmd_name == "COPY":
                if cmd_meta.get_operand().type == "default":
                    self.handle_add_or_copy_eigenvector_with_type_default_by_current_dir(cmd_meta, current_dir)
                else:
                    self.handle_add_or_copy_eigenvector_with_type_other(cmd_meta, current_dir)
                # pass
            elif cmd_name == "RUN":
                current_dir = self.handle_run_eigenvector_by_extractor_way(cmd_meta, current_user, current_dir)
                # pass
            # Tuple
            elif cmd_name == "WORKDIR":
                t = cmd_meta.get_operand().value
                assert len(t) == 1
                path = t[0]
                if os.path.isabs(path) or path[0] == "$":
                    current_dir = path
                else:
                    current_dir = os.path.join(current_dir, path)
                    cmd_meta.operand.set_value(current_dir)
            # Tuple
            elif cmd_name == "USER":
                t = cmd_meta.get_operand().value
                assert len(t) == 1
                current_user = t[0]
            cmd_meta.set_attribute_user(current_user)
            cmd_meta.set_attribute_dir(current_dir)
        return

    def handle_add_or_copy_eigenvector_with_type_default_by_current_dir(self, cmd_meta, current_dir) -> None:
        eigenvector_init: List = cmd_meta.eigenvector_init
        dst_dir_path: str = cmd_meta.get_operand().if_value_is_dir_dict_to_get_dst_dir()
        if len(eigenvector_init) == 1:
            src_path = os.path.join(self.build_ctx, eigenvector_init[0])
            src_file_name = os.path.basename(src_path)
            dst_file_name = os.path.basename(dst_dir_path)
            if os.path.isfile(src_path) and dst_file_name != src_file_name:
                path_list = self.if_src_is_file_but_dst_is_dst(current_dir, src_file_name, dst_dir_path)
            else:
                path_list = self.if_src_dir_path_len_equal_one_and_not_know_src(current_dir, dst_dir_path)
        else:
            path_list = self.if_dst_dir_path_is_directory(eigenvector_init, current_dir, dst_dir_path)
        path_tree: DirectoryTree = DirectoryTree(path_list)
        cmd_meta.set_eigenvector(path_tree)

    def handle_add_or_copy_eigenvector_with_type_other(self, cmd_meta, current_dir) -> None:
        eigenvector_init: List = cmd_meta.eigenvector_init
        dst_dir_path: str = cmd_meta.get_operand().if_value_is_dir_dict_to_get_dst_dir()
        if len(eigenvector_init) == 1:
            src_path_name = eigenvector_init[0]
            dst_file_name = os.path.basename(dst_dir_path)
            if "." in src_path_name and dst_file_name != src_path_name:
                path_list = self.if_src_is_file_but_dst_is_dst(current_dir, src_path_name, dst_dir_path)
            else:
                path_list = self.if_src_dir_path_len_equal_one_and_not_know_src(current_dir, dst_dir_path)
        else:
            path_list = self.if_dst_dir_path_is_directory(eigenvector_init, current_dir, dst_dir_path)
        path_tree: DirectoryTree = DirectoryTree(path_list)
        cmd_meta.set_eigenvector(path_tree)

    @staticmethod
    def if_src_dir_path_len_equal_one_and_not_know_src(current_dir: str, dst_dir_path: str) -> List[str]:
        if os.path.isabs(dst_dir_path) or dst_dir_path[0] == "$":
            path_list = [dst_dir_path]
        else:
            if current_dir[0] == "$":
                dst_dir_path = os.path.normpath(os.path.join(current_dir, dst_dir_path))
            else:
                dst_dir_path = os.path.abspath(os.path.join(current_dir, dst_dir_path))
            path_list = [dst_dir_path]
        return path_list

    @staticmethod
    def if_src_is_file_but_dst_is_dst(current_dir: str, src_file_name: str, dst_dir_path: str) -> List[str]:
        if os.path.isabs(dst_dir_path):
            path_list = [os.path.abspath(os.path.join(dst_dir_path, src_file_name))]
        elif dst_dir_path[0] == "$":
            path_list = [os.path.normpath(os.path.join(dst_dir_path, src_file_name))]
        else:
            if current_dir[0] == "$":
                dst_dir_path = os.path.normpath(os.path.join(current_dir, dst_dir_path))
                path_list = [os.path.normpath(os.path.join(dst_dir_path, src_file_name))]
            else:
                dst_dir_path = os.path.abspath(os.path.join(current_dir, dst_dir_path))
                path_list = [os.path.abspath(os.path.join(dst_dir_path, src_file_name))]
        return path_list

    @staticmethod
    def if_dst_dir_path_is_directory(eigenvector_init: List, current_dir: str, dst_dir_path: str) -> List[str]:
        if os.path.isabs(dst_dir_path):
            path_list = [os.path.abspath(os.path.join(dst_dir_path, src_name)) for src_name in eigenvector_init]
        elif dst_dir_path[0] == "$":
            path_list = [os.path.normpath(os.path.join(dst_dir_path, src_name)) for src_name in eigenvector_init]
        else:
            if current_dir[0] == "$":
                dst_dir_path = os.path.normpath(os.path.join(current_dir, dst_dir_path))
                path_list = [os.path.normpath(os.path.join(dst_dir_path, src_name)) for src_name in eigenvector_init]
            else:
                dst_dir_path = os.path.abspath(os.path.join(current_dir, dst_dir_path))
                path_list = [os.path.abspath(os.path.join(dst_dir_path, src_name)) for src_name in eigenvector_init]
        return path_list

    # Processing shell commands through AST analysis and feature extraction
    @staticmethod
    def handle_run_eigenvector_by_extractor_way(cmd_meta, current_user, current_dir) -> str:
        cmd: str = cmd_meta.get_operand().value
        try:
            instruct_feat_init: InsturctFeatureInit = parse_shell_cmd_to_instruct_feature(cmd)
            if instruct_feat_init:
                cmd_list_feat, attribute_dir = get_command_list_feature(instruct_feat_init.command_list, current_user,
                                                                        current_dir)
                instruct_feat: InstructFeature = InstructFeature(instruct_feat_init, cmd_list_feat, current_user)
                cmd_meta.set_eigenvector(instruct_feat)
                return attribute_dir
            else:
                return current_dir
        except ParsingException:
            raise
        except Exception as e:
            # print(cmd_meta.get_operand().value, file=sys.stderr)
            return current_dir

    @staticmethod
    def strip_without_arg_in_refer_list(arg_list: List, refer_set: Set) -> List:
        return list(set(arg_list) & refer_set)

    @staticmethod
    def strip_parentheses(s: str, arg_list: List) -> str:
        for arg in arg_list:
            pattern = re.compile(r'\${' + arg + r'}')
            s = pattern.sub('$' + arg, s)
        return s
