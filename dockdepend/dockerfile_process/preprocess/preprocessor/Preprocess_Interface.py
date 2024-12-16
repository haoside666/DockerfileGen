from dockerfile import Command
from dockdepend.dockerfile_process.preprocess.datatypes.InstructMetaInit import InstructMetaInit
from dockdepend.dockerfile_process.preprocess.datatypes.Operand import Operand
from dockdepend.exception.CustomizedException import InstructFormatError
from abc import ABC, abstractmethod
from typing import List, Tuple
import glob
import re
import os


class PreprocessInterface(ABC):
    def __init__(self, command: Command, build_ctx: str) -> None:
        self.command: Command = command
        self.build_ctx: str = build_ctx
        self.cmd_meta_init: InstructMetaInit = InstructMetaInit(command.cmd,
                                                                Operand(command.flags, command.sub_cmd, command.value))

    @abstractmethod
    def command_preprocess(self):
        pass

    def preprocess(self):
        self.__get_variable_list()
        self.command_preprocess()

    def get_command_meta(self):
        return self.cmd_meta_init

    def __get_variable_list(self):
        variable_list = re.findall(r"\$[\{a-zA-Z0-9_\}]+", self.command.original)
        if variable_list:
            variable_list = [variable.replace("$", "").replace("{", "").replace("}", "") for variable in variable_list]
        self.cmd_meta_init.set_arg_list(list(set(variable_list)))

    def path_segmentation_for_add_or_copy_instruct(self, path):
        try:
            d = dict()
            d["src_dir"] = path[0:-1]
            d["dst_dir"] = path[-1]
            values = d
            self.cmd_meta_init.get_operand().set_value(values)
        except Exception:
            raise InstructFormatError("add or copy instruct format error")

    def get_add_or_copy_eigenvector_with_type_default(self):
        src_dir_pattern: Tuple = self.cmd_meta_init.get_operand().if_value_is_dir_dict_to_get_src_dir()
        src_dir_list = []
        for pattern in src_dir_pattern:
            # TODO: If no project context is provided, the abs method is used for all.
            #  If it is provided, it is more accurate to use the rel method when the source path is relative.
            src_dir_list.extend(self.__match_files_and_directories_with_abs(pattern))
            # if os.path.isabs(pattern):
            #     src_dir_list.extend(self.__match_files_and_directories_with_abs(pattern))
            # else:
            #     src_dir_list.extend(self.__match_files_and_directories_with_rel(pattern))
        src_dir_set = set(src_dir_list)
        path_list: list[str] = list(src_dir_set)
        self.cmd_meta_init.set_eigenvector_init(path_list)

    # If the source path is in absolute mode
    @staticmethod
    def __match_files_and_directories_with_abs(pattern: str) -> List[str]:
        if pattern[-1] == "/":
            pattern = pattern[:-1]
        return [os.path.basename(pattern)]

    # If the source path is in relative mode, and provides a path context. Solving wildcard problems in paths.
    def __match_files_and_directories_with_rel(self, pattern: str) -> List[str]:
        root_dir = self.build_ctx
        lis = pattern.rsplit("/", maxsplit=1)
        if len(lis) == 2:
            aaa = os.path.join(root_dir, lis[0])
            root_dir = os.path.abspath(aaa)
        pattern = lis[-1]
        match_list = []
        if self.has_glob_wildcard(pattern):
            try:
                if pattern == "*":
                    for path in os.listdir(root_dir):
                        new_path = os.path.abspath(os.path.join(root_dir, path))
                        if os.path.isfile(new_path):
                            match_list.append(os.path.relpath(new_path, root_dir))
                        elif os.path.isdir(new_path):
                            all_list = self.get_all_file_and_dir_in_root_dir(new_path)
                            match_list.extend([os.path.relpath(item, new_path) for item in all_list])
                        else:
                            pass

                else:
                    match_list = glob.glob(os.path.join(root_dir, pattern), recursive=False)
                    match_list = [os.path.relpath(item, root_dir) for item in match_list]
            except:
                return []
        else:
            path = os.path.abspath(os.path.join(root_dir, pattern))
            if os.path.isdir(path):
                match_list = self.get_all_file_and_dir_in_root_dir(path)
                match_list = [os.path.relpath(item, path) for item in match_list]
            elif os.path.isfile(path):
                match_list = [os.path.relpath(path, root_dir)]
            else:
                pass
        return match_list

    @staticmethod
    def has_glob_wildcard(pattern) -> bool:
        # 定义glob.glob支持的通配符正则表达式
        glob_pattern = re.compile(r'[*?\[]')
        return bool(glob_pattern.search(pattern))

    @staticmethod
    def get_all_file_and_dir_in_root_dir(root_dir) -> List[str]:
        all_list = []
        for root, dirs, files in os.walk(root_dir, topdown=False):
            for file_name in files:
                all_list.append(os.path.join(root, file_name))
            for dir_name in dirs:
                all_list.append(os.path.join(root, dir_name))
        return all_list

    @staticmethod
    def match_url_or_git_repository(original: str) -> bool:
        pattern = re.compile(r'(https?://|git@)')
        m = re.search(pattern, original)
        if m is None:
            return False
        else:
            return True
