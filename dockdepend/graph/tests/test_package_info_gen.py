import unittest

from dockdepend.config.definitions import ROOT_DIR

from dockdepend.config import global_config
from dockdepend.dockerfile_process.process import process
from dockdepend.dockerfile_process.datatypes.DockerfilePrimitiveMeta import DockerfilePrimitiveMeta
from dockdepend.dependency.get_dependency_relation import get_dependency_relation
from dockdepend.dependency.datatypes.EdgeIndexList import EdgeIndexList
from typing import Optional
import time
import os
import json
import pandas as pd

from dockdepend.graph.Entity.EntityGen import entity_gen
from dockdepend.graph.Entity.EntityNode import EntityNode
from dockdepend.graph.template.gen_graph import generate_graph_html


class TestGraphInfoGen(unittest.TestCase):
    def test_single_dockerfile(self):
        dockerfile_name = f"{ROOT_DIR}/data/example/aero###1e921f6297c23bed7446f6e909fb01c421985424.txt"
        build_ctx = "/home/haoside/Desktop/aaa"
        dockerfile_meta: Optional[DockerfilePrimitiveMeta] = process(dockerfile_name, build_ctx)
        if dockerfile_meta is not None:
            # print(dockerfile_meta)
            for stage_meta in dockerfile_meta.stage_meta_list:
                edge_index_list: EdgeIndexList = get_dependency_relation(stage_meta)
                node_labels = {}
                for idx, p_meta in enumerate(stage_meta.p_meta_list):
                    entity_node: EntityNode = entity_gen(p_meta)
                    text = entity_node.pretty()
                    node_labels[idx] = f'{idx}-{text[:20]}'
                    print(f"{idx}-{text}")
                edge_list = edge_index_list.transform_to_list_print()
                generate_graph_html(os.path.basename(dockerfile_name), node_labels, edge_list)
                # edge_index_list.pretty()
                print(edge_list)
        else:
            print("process failed")

    # Print only dependency tuples
    def test_single_dockerfile2(self):
        dockerfile_name = f"{ROOT_DIR}/data/Dockerfile3"
        build_ctx = "/home/haoside/Desktop/aaa"
        dockerfile_meta: Optional[DockerfilePrimitiveMeta] = process(dockerfile_name, build_ctx)
        if dockerfile_meta is not None:
            # print(dockerfile_meta)
            for stage_meta in dockerfile_meta.stage_meta_list:
                edge_index_list: EdgeIndexList = get_dependency_relation(stage_meta)
                node_labels = {}
                for idx, p_meta in enumerate(stage_meta.p_meta_list):
                    entity_node: EntityNode = entity_gen(p_meta)
                    text = entity_node.pretty()
                    node_labels[idx] = f'{idx}-{text[:20]}'
                    print(f"{idx}-{text}")
                edge_list = edge_index_list.transform_to_list_print()
                generate_graph_html(os.path.basename(dockerfile_name), node_labels, edge_list)
                # edge_index_list.pretty()

    # Test system stability (Large number of dockerfile samples to test)
    def test_system_stability(self):
        root_dir = "dataset/dataset_all"
        build_ctx = "/home/haoside/Desktop/aaa"

        dirs = os.listdir(root_dir)
        cnt = 0
        for project_name in dirs:
            project_path = os.path.join(root_dir, project_name)
            for filename in os.listdir(project_path):
                print(f"handle: {cnt}---------------")
                cnt += 1
                # control speed
                if cnt % 200 == 0:
                    time.sleep(2)
                file_path = os.path.join(project_path, filename)
                try:
                    dockerfile_meta: Optional[DockerfilePrimitiveMeta] = process(file_path, build_ctx)
                    if dockerfile_meta is not None:
                        for command_meta_list in dockerfile_meta.stage_meta_list:
                            edge_index_list: EdgeIndexList = get_dependency_relation(command_meta_list)
                except Exception:
                    raise
            with open("/home/haoside/Desktop/finish_record.txt", "a") as f:
                print(project_name, file=f)

    # Judging dependencies on a multiple dockerfiles
    # Just set the root_dir and the output_dir
    # root_dir (The input directory contains a large number of dockerfiles)
    # output_dir (Directory for storing the results of judged dependencies)
    def get_multiple_dockerfiles_dependency_info_but_strip_functional_consistency(self):
        # Filtering certain functional consistency types (not part of our defined dependencies)
        filter_list = [
            "exist unrecognised commands, default dependencies exist",
            "Functional dependencies",
            "Additional dependencies to ensure functional consistency"
        ]
        root_dir = "/home/haoside/Desktop/example"
        build_ctx = "/home/haoside/Desktop/aaa"
        output_dir = "/home/haoside/Desktop/stage3"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        for filename in os.listdir(root_dir):
            file_path = os.path.join(root_dir, filename)
            dockerfile_meta: Optional[DockerfilePrimitiveMeta] = process(file_path, build_ctx)
            if dockerfile_meta is not None:
                # print(dockerfile_meta)
                for command_meta_list in dockerfile_meta.stage_meta_list:
                    output_file = os.path.join(output_dir, filename)
                    # beautiful_command_meta_print(command_meta_list, output_file)
                    edge_index_list: EdgeIndexList = get_dependency_relation(command_meta_list)
                    s = ""
                    with open(output_file, "w") as file:
                        new_list = [*zip(edge_index_list.edge_index_list, edge_index_list.msg_list)]
                        s += "[\n"
                        for edge, msg in new_list:
                            if msg not in filter_list:
                                s += f"\t{str(edge)},\t# {msg}\n"
                        s += "]\n"
                        file.write(s)

    def test_get_multiple_dockerfiles_dependency_info(self):
        # Filtering certain functional consistency types (not part of our defined dependencies)
        root_dir = f"{ROOT_DIR}/example"
        build_ctx = "/home/haoside/Desktop/aaa"
        output_dir = "/home/haoside/Desktop/stage3"
        global_config.ignore_unknown_command = True
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        for filename in os.listdir(root_dir):
            file_path = os.path.join(root_dir, filename)
            dockerfile_meta: Optional[DockerfilePrimitiveMeta] = process(file_path, build_ctx)
            if dockerfile_meta is not None:
                # print(dockerfile_meta)
                for command_meta_list in dockerfile_meta.stage_meta_list:
                    output_file = os.path.join(output_dir, filename)
                    # beautiful_command_meta_print(command_meta_list, output_file)
                    edge_index_list: EdgeIndexList = get_dependency_relation(command_meta_list)
                    s = ""
                    with open(output_file, "w") as file:
                        new_list = [
                            *zip(edge_index_list.edge_index_list, edge_index_list.type_list, edge_index_list.msg_list)]
                        s += "[\n"
                        for edge, types, msg in new_list:
                            s += f"\t{str(edge)},\t# {types} {msg}\n"
                        s += "]\n"
                        file.write(s)

    def calc_time(self, fun):
        # 记录程序开始时间
        start_time = time.time()
        fun()
        # 记录程序结束时间
        end_time = time.time()
        # 计算程序运行时间
        run_time = end_time - start_time

        print("程序运行时间为：{:.2f}秒".format(run_time))

    # Printing command meta information in a pretty way for a dockerfile
    def beautiful_command_meta_print(self, command_meta_list, output_json):
        lis = []
        cmd_meta_list = command_meta_list.cmd_meta_list
        for command_mete in cmd_meta_list:
            d = dict()
            d["Original"] = command_mete.pretty()
            d["Meta"] = command_mete.to_dict()
            lis.append(d)
        with open(output_json, "w") as file:
            file.write(json.dumps(lis, indent=4))
