import os.path
import sys
from copy import deepcopy

from graphgen.util import standard_eq

from graphgen.dockerfile_process.datatypes.DirectoryTree import DirectoryTree

from graphgen.config.definitions import IGNORE_DIRECTIVES
from graphgen.dockerfile_process.datatypes.InstructMetaList import InstructMetaList
from graphgen.dockerfile_process.datatypes.ShellFeature import ShellFeature
from graphgen.dockerfile_process.preprocess.datatypes.InstructMeta import InstructMeta
from graphgen.dockerfile_process.preprocess.datatypes.PrimitiveMeta import PrimitiveMeta
from typing import List, Dict, Set, Tuple, Union

from graphgen.exception.CustomizedException import SyntaxNonSupportError, ParsingException
from graphgen.shell_parse.datatypes import PrimitiveFeatureList
from graphgen.shell_parse.datatypes.PrimitiveFeature import PrimitiveFeature
from graphgen.shell_parse.parse import parse_shell_cmd_to_primitive_feature
from graphgen.config.definitions import NOT_CHANGE_DIRECTIVES
from graphgen.extractor.extractor_cli import get_command_list_feature
from graphgen.dockerfile_process.datatypes.InstructFeature import InstructFeature


class PrimitiveMetaList:
    def __init__(self, build_ctx: str, instruct_meta_list: InstructMetaList, postfix="") -> None:
        self.build_ctx: str = build_ctx
        self.postfix: str = postfix
        init_p_meta_list: List[PrimitiveMeta] = self.get_primitive_list(instruct_meta_list)
        self.p_meta_list: List[PrimitiveMeta] = self.__mark_attribute_dir_and_user(init_p_meta_list)

    def __repr__(self):
        repr_str = f'{self.__class__}'
        if len(self.__dict__) != 0:
            repr_str += f': \n'
        else:
            repr_str += f'\n'
        repr_str += f'p_meta_list: \n'
        for item in self.p_meta_list:
            repr_str += f'\t {item.__repr__()}\n'
        return repr_str

    def __str__(self):
        repr_str = f'{self.__class__}'
        if len(self.__dict__) != 0:
            repr_str += f': \n'
        else:
            repr_str += f'\n'
        repr_str += f'p_meta_list: \n'
        for item in self.p_meta_list:
            repr_str += f'\t {item.__str__()}\n'
        return repr_str

    def __eq__(self, other) -> bool:
        return standard_eq(self, other)

    def set_p_meta_list(self, p_meta_list: List[PrimitiveMeta]) -> None:
        self.p_meta_list = p_meta_list

    def length(self) -> int:
        return len(self.p_meta_list)

    def get_primitive_list(self, instruct_meta_list: InstructMetaList) -> List[PrimitiveMeta]:
        cmd_meta_list: List[InstructMeta] = instruct_meta_list.cmd_meta_list
        init_p_meta_list: List[PrimitiveMeta] = []
        for idx, cmd_meta in enumerate(cmd_meta_list):
            cmd_name = cmd_meta.cmd_name
            if cmd_name in IGNORE_DIRECTIVES:
                pass
            elif cmd_name == "RUN":
                init_p_meta_list.extend(self.split_run_instruct(idx, cmd_meta))
            else:
                init_p_meta_list.append(PrimitiveMeta(cmd_meta))

        return init_p_meta_list

    def __mark_attribute_dir_and_user(self, p_meta_list: List[PrimitiveMeta]) -> List[PrimitiveMeta]:
        current_user = "root"
        current_dir = "/"
        for p_meta in p_meta_list:
            cmd_name = p_meta.cmd_name
            if cmd_name in NOT_CHANGE_DIRECTIVES:
                pass
            # Dict
            elif cmd_name == "ADD" or cmd_name == "COPY":
                if p_meta.get_operand().type == "default":
                    self.handle_add_or_copy_eigenvector_with_type_default_by_current_dir(p_meta, current_dir)
                else:
                    self.handle_add_or_copy_eigenvector_with_type_other(p_meta, current_dir)
                # pass
            elif cmd_name == "RUN":
                current_dir = self.handle_run_eigenvector_by_extractor_way(p_meta, current_user, current_dir)
                # pass
            # Tuple
            elif cmd_name == "WORKDIR":
                t = p_meta.get_operand().value
                assert len(t) == 1
                path = t[0]
                if os.path.isabs(path) or path[0] == "$":
                    current_dir = path
                else:
                    current_dir = os.path.join(current_dir, path)
                    p_meta.operand.set_value(current_dir)
            # Tuple
            elif cmd_name == "USER":
                t = p_meta.get_operand().value
                assert len(t) == 1
                current_user = t[0]
            p_meta.set_attribute_user(current_user)
            p_meta.set_attribute_dir(current_dir)
        return p_meta_list

    # 将一个RUN指令拆分成多个RUN指令，以基础命令或管道命令为基元
    def split_run_instruct(self, idx: int, cmd_meta: InstructMeta) -> List[PrimitiveMeta]:
        p_meta_list: List[PrimitiveMeta] = []
        cmd: str = cmd_meta.get_operand().value
        try:
            p_list: Union[str, PrimitiveFeatureList] = parse_shell_cmd_to_primitive_feature(cmd, self.postfix)
            if isinstance(p_list, str):
                if p_list == "None":
                    return p_meta_list
                raise SyntaxNonSupportError(f"{p_list}语法,不用作样本！")
            else:
                p_feat_list: List[PrimitiveFeature] = p_list.p_feat_list
                for p_feat in p_feat_list:
                    p_meta = PrimitiveMeta(cmd_meta)
                    p_meta.set_eigenvector_init(p_feat)
                    p_meta.group = idx
                    p_meta_list.append(p_meta)
                p_meta_list[0].is_master = True
                return p_meta_list
        except ParsingException:
            raise
        except SyntaxNonSupportError:
            raise
        except Exception as e:
            # print(cmd_meta.get_operand().value, file=sys.stderr)
            return p_meta_list

    def handle_add_or_copy_eigenvector_with_type_default_by_current_dir(self, cmd_meta, current_dir) -> None:
        eigenvector_init: List = cmd_meta.eigenvector_init
        dst_dir_path: str = cmd_meta.get_operand().if_value_is_dir_dict_to_get_dst_dir()
        if len(eigenvector_init) == 1:
            src_path = os.path.join(self.build_ctx, eigenvector_init[0])
            src_file_name = os.path.basename(src_path)
            dst_file_name = os.path.basename(dst_dir_path)
            if os.path.isfile(src_path) and dst_file_name != src_file_name:
                path_list = InstructMetaList.if_src_is_file_but_dst_is_dst(current_dir, src_file_name, dst_dir_path)
            else:
                path_list = InstructMetaList.if_src_dir_path_len_equal_one_and_not_know_src(current_dir, dst_dir_path)
        else:
            path_list = InstructMetaList.if_dst_dir_path_is_directory(eigenvector_init, current_dir, dst_dir_path)
        path_tree: DirectoryTree = DirectoryTree(path_list)
        cmd_meta.set_eigenvector(path_tree)

    def handle_add_or_copy_eigenvector_with_type_other(self, cmd_meta, current_dir) -> None:
        eigenvector_init: List = cmd_meta.eigenvector_init
        dst_dir_path: str = cmd_meta.get_operand().if_value_is_dir_dict_to_get_dst_dir()
        if len(eigenvector_init) == 1:
            src_path_name = eigenvector_init[0]
            dst_file_name = os.path.basename(dst_dir_path)
            if "." in src_path_name and dst_file_name != src_path_name:
                path_list = InstructMetaList.if_src_is_file_but_dst_is_dst(current_dir, src_path_name, dst_dir_path)
            else:
                path_list = InstructMetaList.if_src_dir_path_len_equal_one_and_not_know_src(current_dir, dst_dir_path)
        else:
            path_list = InstructMetaList.if_dst_dir_path_is_directory(eigenvector_init, current_dir, dst_dir_path)
        path_tree: DirectoryTree = DirectoryTree(path_list)
        cmd_meta.set_eigenvector(path_tree)

    # Processing shell commands through AST analysis and feature extraction
    @staticmethod
    def handle_run_eigenvector_by_extractor_way(cmd_meta: PrimitiveMeta, current_user, current_dir) -> str:
        try:
            p_feat: PrimitiveFeature = cmd_meta.get_eigenvector_init()
            cmd_list_feat, attribute_dir = get_command_list_feature([p_feat.command], current_user, current_dir)
            shell_feat: ShellFeature = ShellFeature(p_feat, cmd_list_feat, current_user)
            cmd_meta.set_eigenvector(shell_feat)
            return attribute_dir
        except ParsingException:
            raise
        except Exception as e:
            # print(cmd_meta.get_operand().value, file=sys.stderr)
            # return current_dir
            raise
