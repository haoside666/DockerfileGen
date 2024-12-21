from graphgen.config.definitions import URL_DOWNLOAD_COMMAND_SET, UNKNOWN_PREFIX, PKG_CUT_DICT
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
            if pkg_cmd.lower() in PKG_CUT_DICT:
                pkg_list = []
                for item in eigenvector.pkg_set:
                    pkg_name = item[0]
                    if pkg_name not in PKG_CUT_DICT[pkg_cmd.lower()]:
                        pkg_list.append(item)
            else:
                pkg_list = list(eigenvector.pkg_set)
            # 未识别包类型点转换为命令结点
            if len(pkg_list) == 1 and pkg_list[0][0].startswith(UNKNOWN_PREFIX):
                return CommandNode(cmd_list, flags, value, "general")
            cmd_operand_list = [item for item in eigenvector.cmd_operand_list if item not in pkg_list]
            return PkgNode(flags, pkg_cmd, cmd_flag_list, cmd_operand_list, pkg_list)

    def get_cmd_type(self) -> str:
        cmd_type = "general"
        eigenvector: ShellFeature = self.p_meta.eigenvector
        if len(eigenvector.command_set & URL_DOWNLOAD_COMMAND_SET) > 0:
            cmd_type = "url"
        elif len(eigenvector.pkg_set) > 0:
            cmd_type = "pkg"

        return cmd_type
