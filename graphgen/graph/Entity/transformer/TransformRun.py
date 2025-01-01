import logging
import sys

from graphgen.arg_module.graph_module import logger
from graphgen.config.definitions import URL_DOWNLOAD_COMMAND_SET, UNKNOWN_PREFIX, LANGUAGE_SET, ROOT_DIR, SYSTEM_PACKAGE_TOOL_SET
from graphgen.dockerfile_process.datatypes.ShellFeature import ShellFeature
from graphgen.dockerfile_process.preprocess.datatypes.PrimitiveMeta import PrimitiveMeta
from graphgen.graph.Entity.EntityNode import *
from graphgen.graph.Entity.transformer.transform_interface import TransformInterface


class TransformRun(TransformInterface):
    def transform(self) -> EntityNode:
        p_meta: PrimitiveMeta = self.p_meta
        eigenvector: ShellFeature = p_meta.eigenvector
        cmd_list = list(eigenvector.command_set)
        flags = list(p_meta.operand.flags)
        value = eigenvector.command
        cmd_type = self.get_cmd_type()
        if cmd_type == "general":
            return CommandNode(cmd_list, flags, value, cmd_type)
        elif cmd_type == "url":
            return CommandNode(cmd_list, flags, value, cmd_type)
        elif cmd_type == "pkg":
            assert len(cmd_list) == 1
            pkg_set = sorted(list(eigenvector.pkg_set))  # 确保唯一
            # # 未识别包类型结点转换为命令结点
            if len(pkg_set) == 1 and pkg_set[0][0].startswith(UNKNOWN_PREFIX):
                return CommandNode(cmd_list, flags, value, "general")
            pkg_cmd = cmd_list[0]
            cmd_flag_list = eigenvector.cmd_flag_list
            cmd_operand_list = eigenvector.cmd_operand_list
            try:
                # 获取真实的包名，不包括版本信息
                real_pkg_list = self.get_real_pkg_list(cmd_operand_list)
            except:
                print(f"ERROR: 包类型命令含有管道，命令为{eigenvector.command}！", file=sys.stderr)
                logger.error(f"---------------------------------------------")
                logger.error(f"ERROR: 包类型命令含有管道，命令为{eigenvector.command}！")
                logger.error(f"---------------------------------------------")
                real_pkg_list = []
            # 保留人工规则传递出来的包
            pkg_tuple_list = []
            pkg_set = sorted(list(eigenvector.pkg_set))  # 确保唯一
            for item in pkg_set:
                pkg_name = item[0]
                if pkg_name not in LANGUAGE_SET and pkg_name != pkg_cmd:
                    pkg_tuple_list.append(item)
                else:
                    # 去除规则赋予的语言包
                    if pkg_name in real_pkg_list:
                        pkg_tuple_list.append(item)

            if len(pkg_tuple_list) == 0:
                if pkg_cmd not in SYSTEM_PACKAGE_TOOL_SET and eigenvector.input_path_tree.is_not_empty():
                    return FilePkgNode(pkg_cmd, flags, value)
                return CommandNode(cmd_list, flags, value, "general")

            pkg_list = [item[0] for item in pkg_tuple_list]
            version_list = [item[1] for item in pkg_tuple_list]

            return PkgNode(pkg_cmd, flags, cmd_flag_list, cmd_operand_list, pkg_list, version_list)

    def get_cmd_type(self) -> str:
        cmd_type = "general"
        eigenvector: ShellFeature = self.p_meta.eigenvector
        if len(eigenvector.command_set & URL_DOWNLOAD_COMMAND_SET) > 0:
            pattern = r'((https?:\/\/)|(git@))+[^\s]+'
            if re.search(pattern, eigenvector.command):
                cmd_type = "url"
        else:
            if len(eigenvector.pkg_set) > 0:
                # 命令集合大于1的管道命令一定不会是包命令
                if len(eigenvector.command_set) > 1 and "|" in eigenvector.command:
                    with open(f"{ROOT_DIR}/../logs/error.txt", "a") as f:
                        f.write(eigenvector.command + "\n")
                    cmd_type = "general"
                    return cmd_type
                cmd_type = "pkg"

        return cmd_type

    def get_real_pkg_list(self, cmd_operand_list: List[str]) -> List[str]:
        real_pkg_list = [item.split("=")[0] for item in cmd_operand_list]
        return real_pkg_list
