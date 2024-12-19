from graphgen.graph.Entity.EntityNode import *
from graphgen.graph.Entity.transformer.transform_interface import TransformInterface
from graphgen.dockerfile_process.preprocess.datatypes.PrimitiveMeta import PrimitiveMeta


class TransformFrom(TransformInterface):
    def transform(self) -> EntityNode:
        p_meta: PrimitiveMeta = self.p_meta
        flags = p_meta.operand.flags
        value = p_meta.operand.value
        return ImageNode(flags, value)
