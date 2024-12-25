from typing import List

from graphgen.dependency.datatypes.EdgeIndexList import EdgeIndexList, remove_redundant_edges_in_graph
from graphgen.dependency.get_dependency_relation import get_dependency_relation
from graphgen.dockerfile_process.datatypes.PrimitiveMetaList import PrimitiveMetaList
from graphgen.graph.Entity.EntityGen import entity_list_gen
from graphgen.graph.Entity.EntityNode import EntityNode
from graphgen.graph.builds.datatypes.RelationList import RelationList, make_relation_list_from_image_and_execute_node
from graphgen.graph.builds.get_build_info import generate_base_image_and_execute_node, generate_pkg_node_and_cmd_node, generate_tool_node, generate_implicit_node
from graphgen.graph.builds.utils import split_meta_info


# 输入Dockerfile单个阶段的Meta结构，生成其中包含的所有实体和边节点的neo4j脚本
def gen_neo4j_script_by_meta(stage_meta: PrimitiveMetaList) -> str:
    stage_meta, config_meta_list = split_meta_info(stage_meta)
    edge_index_list: EdgeIndexList = get_dependency_relation(stage_meta)
    new_edge_index_list = remove_redundant_edges_in_graph(edge_index_list)
    entity_list = entity_list_gen(stage_meta.p_meta_list)
    config_entity_list = entity_list_gen(config_meta_list)
    img_node, exe_cmd_node_list = generate_base_image_and_execute_node(entity_list, new_edge_index_list)
    r1_list: RelationList = make_relation_list_from_image_and_execute_node(img_node, exe_cmd_node_list)
    r2_list: RelationList = generate_pkg_node_and_cmd_node(entity_list, exe_cmd_node_list)
    r3_list: RelationList = generate_tool_node(entity_list, new_edge_index_list, exe_cmd_node_list, config_entity_list)
    tool_r_list = r1_list + r2_list + r3_list
    neo4j_script = tool_r_list.gen_neo4j_script()
    return neo4j_script
