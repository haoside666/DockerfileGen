from graphgen.dockerfile_process.preprocess.datatypes.PrimitiveMeta import PrimitiveMeta
from graphgen.graph.Entity.EntityNode import *
from graphgen.graph.Entity.transformer.transform_interface import TransformInterface


class TransformArg(TransformInterface):
    def transform(self) -> EntityNode:
        p_meta: PrimitiveMeta = self.p_meta
        flags = p_meta.operand.flags
        value = p_meta.operand.value
        return ArgNode(flags, value)
