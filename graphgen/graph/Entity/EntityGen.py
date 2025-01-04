from typing import List

from graphgen.dockerfile_process.preprocess.datatypes.PrimitiveMeta import PrimitiveMeta
from graphgen.graph.Entity.EntityNode import EntityNode, ConfigNode
from .transformer.TransformFrom import TransformFrom
from .transformer.TransformRun import TransformRun
from .transformer.TransformCmdOrEntrypoint import TransformCmdOrEntrypoint
from .transformer.TransformEnv import TransformEnv
from .transformer.TransformAddOrCopy import TransformAddOrCopy
from .transformer.TransformDefault import TransformDefault
from .transformer.TransformArg import TransformArg

DICT_ENTITY_TYPE_TRANSFORMER_MODULE_MAPPER = {
    'FROM': TransformFrom,
    'RUN': TransformRun,
    'CMD': TransformCmdOrEntrypoint,
    'EXPOSE': TransformDefault,
    'ENV': TransformEnv,
    'ADD': TransformAddOrCopy,
    'COPY': TransformAddOrCopy,
    'ENTRYPOINT': TransformCmdOrEntrypoint,
    'VOLUME': TransformDefault,
    'USER': TransformDefault,
    'WORKDIR': TransformDefault,
    'ARG': TransformArg,
    'SHELL': TransformDefault
}


def entity_gen(p_meta: PrimitiveMeta) -> EntityNode:
    instruct_name = p_meta.cmd_name
    # 得到实体生成类
    entity_gen_class = DICT_ENTITY_TYPE_TRANSFORMER_MODULE_MAPPER[instruct_name]
    entity_gen_object = entity_gen_class(p_meta)
    return entity_gen_object.transform()


def entity_list_gen(p_meta_list: List[PrimitiveMeta]) -> List[EntityNode]:
    entity_list: List[EntityNode] = []
    for p_meta in p_meta_list:
        entity_list.append(entity_gen(p_meta))
    return entity_list


def config_entity_list_gen(p_meta_list: List[PrimitiveMeta]) -> List[ConfigNode]:
    entity_list: List[ConfigNode] = []
    for p_meta in p_meta_list:
        entity = entity_gen(p_meta)
        config_entity = ConfigNode(entity)
        entity_list.append(config_entity)
    return entity_list
