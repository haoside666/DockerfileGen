from typing import List

from graphgen.dependency.datatypes.EdgeIndexList import EdgeIndexList
from graphgen.dependency.get_dependency_relation import get_dependency_relation
from graphgen.dockerfile_process.datatypes.PrimitiveMetaList import PrimitiveMetaList
from graphgen.exception.CustomizedException import PkgNotFoundError
from graphgen.graph.Entity.EntityGen import entity_list_gen, config_entity_list_gen
from graphgen.graph.Entity.EntityNode import EntityNode
from graphgen.graph.builds.datatypes.RelationList import RelationList, make_relation_list_from_image_and_execute_node
from graphgen.graph.builds.get_build_info import generate_base_image_and_execute_node, generate_pkg_node_and_cmd_node, generate_tool_node, generate_file_pkg_node
from graphgen.graph.builds.utils import split_meta_info


# 输入Dockerfile单个阶段的Meta结构，生成其中包含的所有实体和边节点的neo4j脚本
def gen_neo4j_script_by_meta(stage_meta: PrimitiveMetaList, file_path="") -> str:
    # 拆分并去重Meta结构，得到stage_meta和config_meta_list
    stage_meta, config_meta_list = split_meta_info(stage_meta)
    edge_index_list: EdgeIndexList = get_dependency_relation(stage_meta)
    # new_edge_index_list = remove_redundant_edges_in_graph(edge_index_list)，放置到生成工具包节点内部
    entity_list = entity_list_gen(stage_meta.p_meta_list)
    config_entity_list = config_entity_list_gen(config_meta_list)
    # 注意这里需要传入edge_index_list,而不是去重之后的,因为去重后只保留了最近依赖关系
    img_node, exe_cmd_node_list = generate_base_image_and_execute_node(entity_list, edge_index_list)
    r1_list: RelationList = make_relation_list_from_image_and_execute_node(img_node, exe_cmd_node_list)
    r2_list: RelationList = generate_pkg_node_and_cmd_node(entity_list, exe_cmd_node_list)
    r3_list: RelationList = generate_file_pkg_node(entity_list, edge_index_list, img_node, config_entity_list)
    r4_list: RelationList = generate_tool_node(entity_list, edge_index_list, exe_cmd_node_list, config_entity_list, file_path)
    tool_r_list = r1_list + r2_list + r3_list + r4_list
    neo4j_script = tool_r_list.gen_neo4j_script()
    return neo4j_script
