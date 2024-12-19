from graphgen.dockerfile_process.preprocess.datatypes.PrimitiveMeta import PrimitiveMeta
from graphgen.graph.Entity.EntityNode import *
from graphgen.graph.Entity.transformer.transform_interface import TransformInterface


class TransformAddOrCopy(TransformInterface):
    def transform(self) -> EntityNode:
        p_meta: PrimitiveMeta = self.p_meta
        flags = list(p_meta.operand.flags)
        value = p_meta.operand.value
        types = p_meta.operand.type
        return AddOrCopyNode(flags, value, types)
