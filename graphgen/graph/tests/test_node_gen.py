import unittest

from graphgen.config.definitions import ROOT_DIR

from graphgen.dockerfile_process.process import process
from graphgen.dockerfile_process.datatypes.DockerfilePrimitiveMeta import DockerfilePrimitiveMeta
from typing import Optional

from graphgen.graph.Entity.EntityGen import entity_gen
from graphgen.graph.build.datatypes.RelationList import *
from graphgen.graph.build.get_build_info import strip_redundant_node, generate_base_image_and_execute_node, generate_pkg_node_and_cmd_node, generate_tool_node


class TestNodeGen(unittest.TestCase):
    def test_single_dockerfile(self):
        dockerfile_name = f"{ROOT_DIR}/data/Dockerfile_test"
        build_ctx = "/home/haoside/Desktop/aaa"
        dockerfile_meta: Optional[DockerfilePrimitiveMeta] = process(dockerfile_name, build_ctx)
        if dockerfile_meta is not None:
            for stage_meta in dockerfile_meta.stage_meta_list:
                entity_list = []
                for p_meta in stage_meta.p_meta_list:
                    entity_node: EntityNode = entity_gen(p_meta)
                    # print(entity_node.pretty())
                    entity_list.append(entity_node)
                new_entity_node = strip_redundant_node(entity_list)
                img_node, exe_cmd_node_list = generate_base_image_and_execute_node(new_entity_node)
                r_list: RelationList = make_relation_list_from_image_and_execute_node(img_node, exe_cmd_node_list)
                print(r_list)
                r2_list: RelationList = generate_pkg_node_and_cmd_node(new_entity_node, exe_cmd_node_list)
                print(r2_list)

    def test_single_dockerfile2(self):
        dockerfile_name = f"{ROOT_DIR}/data/Dockerfile_test"
        build_ctx = "/home/haoside/Desktop/aaa"
        dockerfile_meta: Optional[DockerfilePrimitiveMeta] = process(dockerfile_name, build_ctx)
        if dockerfile_meta is not None:
            for stage_meta in dockerfile_meta.stage_meta_list:
                entity_list = []
                for p_meta in stage_meta.p_meta_list:
                    entity_node: EntityNode = entity_gen(p_meta)
                    # print(entity_node.pretty())
                    entity_list.append(entity_node)
                new_entity_node = strip_redundant_node(entity_list)
                img_node, exe_cmd_node_list = generate_base_image_and_execute_node(new_entity_node)
                r_list: RelationList = make_relation_list_from_image_and_execute_node(img_node, exe_cmd_node_list)
                print(r_list)
                print(r_list.gen_neo4j_script())
                # r2_list: RelationList = generate_pkg_node_and_cmd_node(new_entity_node, exe_cmd_node_list)
                # print(r2_list)
