import sys

from graphgen.config.definitions import URL_DOWNLOAD_COMMAND_SET, UNKNOWN_PREFIX, LANGUAGE_SET
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
            pkg_cmd = cmd_list[0]
            cmd_flag_list = eigenvector.cmd_flag_list
            cmd_operand_list = eigenvector.cmd_operand_list
            try:
                real_pkg_list = self.get_real_pkg_list(cmd_operand_list)
            except:
                print("ERROR: 包类型命令含有管道！", file=sys.stderr)
                real_pkg_list = []
            # 保留人工规则传递出来的包
            pkg_tuple_list = []
            for item in eigenvector.pkg_set:
                pkg_name = item[0]
                # 去除规则赋予的语言包
                if pkg_name not in LANGUAGE_SET and pkg_name != pkg_cmd:
                    pkg_tuple_list.append(item)
                else:
                    if pkg_name in real_pkg_list:
                        pkg_tuple_list.append(item)
            # 未识别包类型点转换为命令结点
            if len(pkg_tuple_list) == 1 and pkg_tuple_list[0][0].startswith(UNKNOWN_PREFIX):
                return CommandNode(cmd_list, flags, value, "general")
            pkg_list = [item[0] for item in pkg_tuple_list]
            version_list = [item[1] for item in pkg_tuple_list]

            return PkgNode(flags, pkg_cmd, cmd_flag_list, cmd_operand_list, pkg_list, version_list)

    def get_cmd_type(self) -> str:
        cmd_type = "general"
        eigenvector: ShellFeature = self.p_meta.eigenvector
        if len(eigenvector.command_set & URL_DOWNLOAD_COMMAND_SET) > 0:
            pattern = r'((https?:\/\/)|(git@))+[^\s]+'
            if re.search(pattern, eigenvector.command):
                cmd_type = "url"
        elif len(eigenvector.pkg_set) > 0:
            # 管道命令一定不会是包命令
            assert "|" not in eigenvector.command
            cmd_type = "pkg"

        return cmd_type

    def get_real_pkg_list(self, cmd_operand_list: List[str]) -> List[str]:
        real_pkg_list = [item.split("=")[0] for item in cmd_operand_list]
        return real_pkg_list
