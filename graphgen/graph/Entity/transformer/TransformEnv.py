from graphgen.dockerfile_process.preprocess.datatypes.PrimitiveMeta import PrimitiveMeta
from graphgen.graph.Entity.EntityNode import *
from graphgen.graph.Entity.transformer.transform_interface import TransformInterface


class TransformEnv(TransformInterface):
    def transform(self) -> EntityNode:
        p_meta: PrimitiveMeta = self.p_meta
        flags = list(p_meta.operand.flags)
        value: Dict = p_meta.operand.value
        var_info = []
        for key, value in value.items():
            var_info.append(f'{key}="{value}"')
        return EnvNode(flags, sorted(var_info))
