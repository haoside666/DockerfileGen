from typing import List

from graphgen.dependency.datatypes.EdgeIndexList import EdgeIndexList
from graphgen.dependency.get_dependency_relation import get_dependency_relation
from graphgen.dockerfile_process.datatypes.PrimitiveMetaList import PrimitiveMetaList
from graphgen.graph.Entity.EntityGen import entity_gen
from graphgen.graph.Entity.EntityNode import EntityNode
from graphgen.graph.build.datatypes.RelationList import RelationList, make_relation_list_from_image_and_execute_node
from graphgen.graph.build.get_build_info import generate_base_image_and_execute_node, generate_pkg_node_and_cmd_node, generate_tool_node, generate_implicit_node
from graphgen.graph.build.utils import strip_redundant_meta_info


# 输入Dockerfile单个阶段的Meta结构，生成其中包含的所有实体和边节点的neo4j脚本
def gen_neo4j_script_by_meta(stage_meta: PrimitiveMetaList) -> str:
    entity_list: List[EntityNode] = []
    stage_meta = strip_redundant_meta_info(stage_meta)
    edge_index_list: EdgeIndexList = get_dependency_relation(stage_meta)
    for p_meta in stage_meta.p_meta_list:
        entity_node: EntityNode = entity_gen(p_meta)
        entity_list.append(entity_node)
    img_node, exe_cmd_node_list = generate_base_image_and_execute_node(entity_list, edge_index_list)
    r1_list: RelationList = make_relation_list_from_image_and_execute_node(img_node, exe_cmd_node_list)
    r2_list: RelationList = generate_pkg_node_and_cmd_node(entity_list, exe_cmd_node_list)
    r3_list: RelationList = generate_tool_node(entity_list, edge_index_list, exe_cmd_node_list)
    tool_r_list = r1_list + r2_list + r3_list
    neo4j_script = tool_r_list.gen_neo4j_script()
    return neo4j_script
