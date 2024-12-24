from copy import deepcopy

from graphgen.config.definitions import PKG_DIRECTIVES, CONFIG_DIRECTIVES
from graphgen.dockerfile_process.datatypes.PrimitiveMetaList import PrimitiveMetaList
from graphgen.dockerfile_process.preprocess.datatypes.PrimitiveMeta import PrimitiveMeta
from graphgen.graph.Entity.EntityNode import *


def strip_redundant_entity_node(entity_list: List[EntityNode]):
    new_entity_list: List[EntityNode] = []
    for entity_node in entity_list:
        if isinstance(entity_node, DefaultNode) or isinstance(entity_node, BootNode) \
                or isinstance(entity_node, ArgNode) or isinstance(entity_node, EnvNode):
            continue
        else:
            new_entity_list.append(entity_node)
    return new_entity_list


def split_meta_info(stage_meta: PrimitiveMetaList) -> Tuple[PrimitiveMetaList, List[PrimitiveMeta]]:
    new_p_meta_list = deepcopy(stage_meta)
    p_meta_list: List[PrimitiveMeta] = []
    c_meta_list: List[PrimitiveMeta] = []
    for p_meta in new_p_meta_list.p_meta_list:
        if p_meta.cmd_name in PKG_DIRECTIVES:
            p_meta_list.append(p_meta)
        elif p_meta.cmd_name in CONFIG_DIRECTIVES:
            c_meta_list.append(p_meta)
    new_p_meta_list.set_p_meta_list(p_meta_list)
    return new_p_meta_list, c_meta_list
