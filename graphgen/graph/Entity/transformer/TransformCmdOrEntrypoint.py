from graphgen.dockerfile_process.preprocess.datatypes.PrimitiveMeta import PrimitiveMeta
from graphgen.graph.Entity.EntityNode import *
from graphgen.graph.Entity.transformer.transform_interface import TransformInterface


class TransformCmdOrEntrypoint(TransformInterface):
    def transform(self) -> EntityNode:
        p_meta: PrimitiveMeta = self.p_meta
        instruct_name = p_meta.cmd_name
        flags = list(p_meta.operand.flags)
        value = list(p_meta.operand.value)
        return BootNode(instruct_name, flags, value)
