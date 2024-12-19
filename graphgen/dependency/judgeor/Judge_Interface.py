from abc import ABC, abstractmethod
from graphgen.dockerfile_process.preprocess.datatypes.PrimitiveMeta import PrimitiveMeta
from graphgen.dockerfile_process.datatypes.DirectoryTree import DirectoryTree, trees_have_intersection, \
    path_have_intersection_with_tree
from graphgen.dockerfile_process.datatypes.InsturctFeature import InstructFeature
from typing import Tuple, Set, Optional
from graphgen.config.system_env import SYSTEM_ENV_DICT
from graphgen.config.definitions import PROGRAM_COMMAND_SET, DIR_COMMAND_SET, side_effect_command_set
from graphgen.dependency.datatypes.DDType import DDType
from graphgen.config import global_config


class JudgeInterface(ABC):
    def __init__(self, command_meta1: PrimitiveMeta, command_meta2: PrimitiveMeta) -> None:
        self.command_meta1: PrimitiveMeta = command_meta1
        self.command_meta2: PrimitiveMeta = command_meta2

    @abstractmethod
    def get_dependence(self) -> Tuple[DDType, str]:
        pass

    def get_common_arg_dependence(self) -> Tuple[DDType, str]:
        arg_list1 = self.command_meta1.get_operand().if_value_is_dict_to_get_keys()
        arg_list2 = self.command_meta2.get_arg_list()
        for arg in arg_list2:
            if arg in arg_list1:
                return DDType.ENV_VAR, "environment variable dependencies"
        return DDType.NONE, ""

    # ENV RUN or ARG RUN
    def get_special_env_with_run_dependence(self) -> Tuple[DDType, str]:
        env_set: Set = set(self.command_meta1.get_operand().if_value_is_dict_to_get_keys())
        instruct_feat: Optional[InstructFeature] = self.command_meta2.get_eigenvector()
        if instruct_feat is None:
            return DDType.NONE, ""
        else:
            cmd_set: Set = instruct_feat.command_set
            union_set: Set = cmd_set & set(SYSTEM_ENV_DICT.keys())
            if len(union_set) > 0:
                for cmd in union_set:
                    if len(env_set & SYSTEM_ENV_DICT[cmd]) > 0:
                        return DDType.ENV_VAR_IMPLICIT, "system level environment variable dependencies(implicit)"
            return DDType.NONE, ""

    def get_add_or_copy_with_run_dependence(self) -> Tuple[DDType, str]:
        path_tree: DirectoryTree = self.command_meta1.get_eigenvector()
        instruct_feat: Optional[InstructFeature] = self.command_meta2.get_eigenvector()

        if instruct_feat is None or path_tree is None:
            return DDType.NONE, ""
        else:
            flag, common_path = trees_have_intersection(path_tree, instruct_feat.input_path_tree)
            if flag:
                common_path = f'exist file or directory dependency,because common path {common_path}'
                return DDType.FILE_DIR, common_path
            return DDType.NONE, common_path

    def get_add_or_copy_with_workdir_dependence(self) -> Tuple[DDType, str]:
        # Add or Copy
        path_tree: DirectoryTree = self.command_meta1.get_eigenvector()
        # workdir
        dir_list: Tuple[str] = self.command_meta2.get_operand().value
        if path_tree is None:
            return DDType.NONE, "",
        for dir_path in dir_list:
            if not path_have_intersection_with_tree(dir_path, path_tree):
                return DDType.FILE_DIR, "exist file or directory dependency"
        return DDType.NONE, ""

    # VOLUME RUN or WORKDIR RUN
    def get_dir_list_with_run_dependence(self) -> Tuple[DDType, str]:
        dir_list: Tuple[str] = self.command_meta1.get_operand().value
        instruct_feat: Optional[InstructFeature] = self.command_meta2.get_eigenvector()
        if instruct_feat is None:
            return DDType.NONE, ""
        else:
            search_tree = instruct_feat.input_path_tree
            for dir_path in dir_list:
                if path_have_intersection_with_tree(dir_path, search_tree):
                    return DDType.FILE_DIR, f"exist file or directory dependency,because RUN instruct use {dir_path}"
            command_set = instruct_feat.command_set
            # 进行一致性依赖判断
            if global_config.show_consistency_dependency:
                if len(DIR_COMMAND_SET & command_set) > 0:
                    search_tree = instruct_feat.output_path_tree
                    for dir_path in dir_list:
                        if path_have_intersection_with_tree(dir_path, search_tree):
                            return DDType.CONSISTENCY, "consistency dependency"
            return DDType.NONE, ""

            # RUN WORKDIR

    def get_run_with_dir_dependence(self) -> Tuple[DDType, str]:
        instruct_feat: Optional[InstructFeature] = self.command_meta1.get_eigenvector()
        dir_list: Tuple[str] = self.command_meta2.get_operand().value
        if instruct_feat is None:
            return DDType.NONE, ""
        else:
            command_set = instruct_feat.command_set
            search_tree = instruct_feat.output_path_tree
            for dir_path in dir_list:
                if path_have_intersection_with_tree(dir_path, search_tree):
                    return DDType.FILE_DIR, f"exist file or directory dependency,because RUN instruct create {dir_path}"
            # 进行一致性依赖判断
            if global_config.show_consistency_dependency:
                if len(DIR_COMMAND_SET & command_set) > 0:
                    if not instruct_feat.output_path_tree.is_empty():
                        return DDType.CONSISTENCY, "consistency dependency,File system impact dependencies",
                elif len(PROGRAM_COMMAND_SET & command_set) > 0:
                    return DDType.CONSISTENCY, "consistency dependency,File system impact dependencies"
            return DDType.NONE, ""
