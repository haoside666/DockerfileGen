from dockdepend.dockerfile_process.preprocess.datatypes.PrimitiveMeta import PrimitiveMeta
from dockdepend.graph.Entity.EntityNode import *
from dockdepend.graph.Entity.transformer.transform_interface import TransformInterface


class TransformAddOrCopy(TransformInterface):
    def transform(self) -> EntityNode:
        p_meta: PrimitiveMeta = self.p_meta
        flags = p_meta.operand.flags
        value = p_meta.operand.value
        types = p_meta.operand.type
        return AddOrCopyNode(flags, value, types)
