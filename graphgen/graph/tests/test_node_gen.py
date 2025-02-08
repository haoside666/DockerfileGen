import os
import unittest

from graphgen.config.definitions import ROOT_DIR
from graphgen.dependency.datatypes.EdgeIndexList import EdgeIndexList
from graphgen.dependency.get_dependency_relation import get_dependency_relation

from graphgen.dockerfile_process.processer import processer
from graphgen.dockerfile_process.datatypes.DockerfilePrimitiveMeta import DockerfilePrimitiveMeta
from typing import Optional

from graphgen.graph.Entity.EntityGen import entity_gen, entity_list_gen, config_entity_list_gen
from graphgen.graph.builds.datatypes.RelationList import *
from graphgen.graph.builds.get_build_info import generate_base_image_and_execute_node, generate_pkg_node_and_cmd_node, generate_tool_node, generate_file_pkg_node
from graphgen.graph.builds.neo4j_reader import Neo4jConnection
from graphgen.graph.builds.utils import strip_redundant_entity_node, split_meta_info


class TestNodeGen(unittest.TestCase):
    def test_cmd_node_gen(self):
        dockerfile_name = f"{ROOT_DIR}/data/Dockerfile_test"
        build_ctx = "/home/haoside/Desktop/aaa"
        dockerfile_meta: Optional[DockerfilePrimitiveMeta] = processer(dockerfile_name, build_ctx)
        if dockerfile_meta is not None:
            for stage_meta in dockerfile_meta.stage_meta_list:
                entity_list = []
                edge_index_list: EdgeIndexList = get_dependency_relation(stage_meta)
                for p_meta in stage_meta.p_meta_list:
                    entity_node: EntityNode = entity_gen(p_meta)
                    print(entity_node.pretty())
                    entity_list.append(entity_node)
                img_node, exe_cmd_node_list = generate_base_image_and_execute_node(entity_list, edge_index_list)
                r_list: RelationList = make_relation_list_from_image_and_execute_node(img_node, exe_cmd_node_list)
                print(r_list)

    def test_pkg_node_gen(self):
        dockerfile_name = f"{ROOT_DIR}/data/Dockerfile_test"
        build_ctx = "/home/haoside/Desktop/aaa"
        dockerfile_meta: Optional[DockerfilePrimitiveMeta] = processer(dockerfile_name, build_ctx)
        if dockerfile_meta is not None:
            for stage_meta in dockerfile_meta.stage_meta_list:
                entity_list = []
                stage_meta, _ = split_meta_info(stage_meta)
                edge_index_list: EdgeIndexList = get_dependency_relation(stage_meta)
                for p_meta in stage_meta.p_meta_list:
                    entity_node: EntityNode = entity_gen(p_meta)
                    print(entity_node.pretty())
                    entity_list.append(entity_node)
                img_node, exe_cmd_node_list = generate_base_image_and_execute_node(entity_list, edge_index_list)
                r_list: RelationList = make_relation_list_from_image_and_execute_node(img_node, exe_cmd_node_list)
                print(r_list)
                r2_list = generate_pkg_node_and_cmd_node(entity_list, exe_cmd_node_list)
                print(r2_list)
                union_r_list: RelationList = r_list + r2_list
                with open(f"{ROOT_DIR}/graph/script/script.cypher", "w") as file:
                    file.write(union_r_list.gen_neo4j_script())

                conn = Neo4jConnection()
                with open(f"{ROOT_DIR}/graph/script/script.cypher", "r") as file:
                    cypher_script = file.read()
                conn.run_script(cypher_script)
                conn.close()

    def test_single_dockerfile(self):
        # dockerfile_name = f"/home/haoside/Desktop/output/leejoneshane___ezgo-vdi###1343644###70579ac9688627897b3050f82dfaaf1547cdc365_script.cypher"
        dockerfile_name = f"{ROOT_DIR}/data/Dockerfile_all_instruction"
        build_ctx = "/home/haoside/Desktop/aaa"
        dockerfile_meta: Optional[DockerfilePrimitiveMeta] = processer(dockerfile_name, build_ctx)
        if dockerfile_meta is not None:
            for stage_meta in dockerfile_meta.stage_meta_list:
                stage_meta, config_meta_list = split_meta_info(stage_meta)
                edge_index_list: EdgeIndexList = get_dependency_relation(stage_meta)
                entity_list = entity_list_gen(stage_meta.p_meta_list)
                config_entity_list = config_entity_list_gen(config_meta_list)
                img_node, exe_cmd_node_list = generate_base_image_and_execute_node(entity_list, edge_index_list)
                r1_list: RelationList = make_relation_list_from_image_and_execute_node(img_node, exe_cmd_node_list)
                print(r1_list)
                r2_list: RelationList = generate_pkg_node_and_cmd_node(entity_list, exe_cmd_node_list)
                print(r2_list)
                r3_list: RelationList = generate_file_pkg_node(entity_list, edge_index_list, img_node, config_entity_list)
                print(r3_list)
                r4_list: RelationList = generate_tool_node(entity_list, edge_index_list, exe_cmd_node_list, config_entity_list, dockerfile_name)
                print(r4_list)
                tool_r_list = r1_list + r2_list + r3_list + r4_list
                with open(f"{ROOT_DIR}/graph/script/{os.path.basename(dockerfile_name)}.cypher", "w") as file:
                    script_str = tool_r_list.gen_neo4j_script()
                    file.write(script_str)
                    print(script_str)

                conn = Neo4jConnection()
                with open(f"{ROOT_DIR}/graph/script/{os.path.basename(dockerfile_name)}.cypher", "r") as file:
                    cypher_script = file.read()
                conn.run_script(cypher_script)
                conn.close()
