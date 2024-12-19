from graphgen.config.definitions import URL_DOWNLOAD_COMMAND_SET, UNKNOWN_PREFIX
from graphgen.dockerfile_process.datatypes.ShellFeature import ShellFeature
from graphgen.dockerfile_process.preprocess.datatypes.PrimitiveMeta import PrimitiveMeta
from graphgen.graph.Entity.EntityNode import *
from graphgen.graph.Entity.transformer.transform_interface import TransformInterface


class TransformRun(TransformInterface):
    def transform(self) -> EntityNode:
        p_meta: PrimitiveMeta = self.p_meta
        eigenvector: ShellFeature = p_meta.eigenvector
        cmd_set = eigenvector.command_set
        flags = list(p_meta.operand.flags)
        value = eigenvector.command
        cmd_type = self.get_cmd_type()
        if cmd_type == "general":
            return CommandNode(cmd_set, flags, value, cmd_type)
        elif cmd_type == "url":
            return CommandNode(cmd_set, flags, value, cmd_type)
        elif cmd_type == "pkg":
            assert len(cmd_set) == 1
            pkg_cmd = list(cmd_set)[0]
            cmd_flag_list = eigenvector.cmd_flag_list
            pkg_set = eigenvector.pkg_set & set(eigenvector.cmd_operand_list)
            # 未识别包类型点转换为命令结点
            if len(pkg_set) == 1 and list(pkg_set)[0].startswith(UNKNOWN_PREFIX):
                return CommandNode(cmd_set, flags, value, "general")
            cmd_operand_list = [item for item in eigenvector.cmd_operand_list if item not in pkg_set]
            return PkgNode(flags, pkg_cmd, cmd_flag_list, cmd_operand_list, pkg_set)

    def get_cmd_type(self) -> str:
        cmd_type = "general"
        eigenvector: ShellFeature = self.p_meta.eigenvector
        if len(eigenvector.command_set & URL_DOWNLOAD_COMMAND_SET) > 0:
            cmd_type = "url"
        elif len(eigenvector.pkg_set) > 0:
            cmd_type = "pkg"

        return cmd_type
