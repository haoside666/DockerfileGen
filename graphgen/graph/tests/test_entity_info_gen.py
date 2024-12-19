import unittest

from graphgen.config.definitions import ROOT_DIR

from graphgen.dockerfile_process.process import process
from graphgen.dockerfile_process.datatypes.DockerfilePrimitiveMeta import DockerfilePrimitiveMeta
from typing import Optional

from graphgen.graph.Entity.EntityGen import entity_gen
from graphgen.graph.Entity.EntityNode import EntityNode


class TestEntityInfoGen(unittest.TestCase):
    def test_single_dockerfile(self):
        dockerfile_name = f"{ROOT_DIR}/data/Dockerfile3"
        build_ctx = "/home/haoside/Desktop/aaa"
        dockerfile_meta: Optional[DockerfilePrimitiveMeta] = process(dockerfile_name, build_ctx)
        if dockerfile_meta is not None:
            for stage_meta in dockerfile_meta.stage_meta_list:
                for p_meta in stage_meta.p_meta_list:
                    entity_node: EntityNode = entity_gen(p_meta)
                    print(entity_node.pretty())
                    print(entity_node)

    def test_single_dockerfile2(self):
        dockerfile_name = f"{ROOT_DIR}/data/example/aero###1e921f6297c23bed7446f6e909fb01c421985424.txt"
        build_ctx = "/home/haoside/Desktop/aaa"
        dockerfile_meta: Optional[DockerfilePrimitiveMeta] = process(dockerfile_name, build_ctx)
        if dockerfile_meta is not None:
            for stage_meta in dockerfile_meta.stage_meta_list:
                for p_meta in stage_meta.p_meta_list:
                    entity_node: EntityNode = entity_gen(p_meta)
                    print(entity_node.pretty())
