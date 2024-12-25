import json
import pathlib
import unittest
import os

from graphgen.config.definitions import ROOT_DIR

from graphgen.dockerfile_process.datatypes.PrimitiveMetaList import PrimitiveMetaList
from graphgen.dockerfile_process.processer import processer
from graphgen.dockerfile_process.datatypes.DockerfilePrimitiveMeta import DockerfilePrimitiveMeta
from typing import Optional, List




# Printing command meta information in a pretty way for a dockerfile
def beautiful_command_meta_print(p_meta_list: PrimitiveMetaList, out_path, current_num=1, stage_num=1):
    lis = []
    cmd_meta_list = p_meta_list.p_meta_list
    for command_mete in cmd_meta_list:
        d = dict()
        d["Original"] = command_mete.pretty()
        d["Meta"] = command_mete.to_dict()
        lis.append(d)
    if stage_num == 1:
        with open(out_path, "w") as file:
            file.write(json.dumps(lis, indent=4))
    else:
        base_name, ext = os.path.splitext(out_path)
        out_path = f'{base_name}_{current_num}{ext}'
        with open(out_path, "w") as file:
            file.write(json.dumps(lis, indent=4))


class TestMeta(unittest.TestCase):
    def test_process_dockerfile1(self):
        filename = "Dockerfile_test_add"
        dockerfile_name = f"{ROOT_DIR}/data/{filename}"
        build_ctx = "/home/haoside/Desktop/aaa"
        dockerfile_meta: Optional[DockerfilePrimitiveMeta] = processer(dockerfile_name, build_ctx)
        if dockerfile_meta is not None:
            stage_num = len(dockerfile_meta.stage_meta_list)
            for i in range(stage_num):
                p_meta_list: PrimitiveMetaList = dockerfile_meta.stage_meta_list[i]
                beautiful_command_meta_print(p_meta_list, f"./output/{filename}_meta.json", i + 1, stage_num)
            print(dockerfile_meta)

    def test_process_dockerfile2(self):
        filename = "Dockerfile3"
        dockerfile_name = f"{ROOT_DIR}/data/{filename}"
        build_ctx = "/home/haoside/Desktop/aaa"
        dockerfile_meta: Optional[DockerfilePrimitiveMeta] = processer(dockerfile_name, build_ctx)
        if dockerfile_meta is not None:
            stage_num = len(dockerfile_meta.stage_meta_list)
            for i in range(stage_num):
                command_meta_list = dockerfile_meta.stage_meta_list[i]
                beautiful_command_meta_print(command_meta_list, f"./output/{filename}_meta.json", i + 1, stage_num)
            print(dockerfile_meta)

    def test_process_dockerfile3(self):
        filename = "Dockerfile3"
        dockerfile_name = f"{ROOT_DIR}/data/{filename}"
        build_ctx = "/home/haoside/Desktop/aaa"
        dockerfile_meta: Optional[DockerfilePrimitiveMeta] = processer(dockerfile_name, build_ctx)
        if dockerfile_meta is not None:
            stage_num = len(dockerfile_meta.stage_meta_list)
            for i in range(stage_num):
                command_meta_list = dockerfile_meta.stage_meta_list[i]
                beautiful_command_meta_print(command_meta_list, f"./output/{filename}_meta.json", i + 1, stage_num)
            print(dockerfile_meta)

    def test_process_dockerfile4(self):
        filename = "Dockerfile4"
        dockerfile_name = f"{ROOT_DIR}/data/{filename}"
        build_ctx = "/home/haoside/Desktop/aaa"
        dockerfile_meta: Optional[DockerfilePrimitiveMeta] = processer(dockerfile_name, build_ctx)
        if dockerfile_meta is not None:
            stage_num = len(dockerfile_meta.stage_meta_list)
            for i in range(stage_num):
                command_meta_list = dockerfile_meta.stage_meta_list[i]
                beautiful_command_meta_print(command_meta_list, f"./output/{filename}_meta.json", i + 1, stage_num)
            print(dockerfile_meta)

    def test_process_mutil_dockerfile1(self):
        filename = "Dockerfile5"
        dockerfile_name = f"{ROOT_DIR}/data/{filename}"
        build_ctx = "/home/haoside/Desktop/aaa"
        dockerfile_meta: Optional[DockerfilePrimitiveMeta] = processer(dockerfile_name, build_ctx)
        if dockerfile_meta is not None:
            stage_num = len(dockerfile_meta.stage_meta_list)
            for i in range(stage_num):
                command_meta_list = dockerfile_meta.stage_meta_list[i]
                beautiful_command_meta_print(command_meta_list, f"./output/{filename}_meta.json", i + 1, stage_num)
            print(dockerfile_meta)

    def test_process_mutil_dockerfile2(self):
        filename = "Dockerfile_mutil"
        dockerfile_name = f"{ROOT_DIR}/data/{filename}"
        build_ctx = "/home/haoside/Desktop/aaa"
        dockerfile_meta: Optional[DockerfilePrimitiveMeta] = processer(dockerfile_name, build_ctx)
        if dockerfile_meta is not None:
            stage_num = len(dockerfile_meta.stage_meta_list)
            for i in range(stage_num):
                command_meta_list = dockerfile_meta.stage_meta_list[i]
                beautiful_command_meta_print(command_meta_list, f"./output/{filename}_meta.json", i + 1, stage_num)
            print(dockerfile_meta)

    # def test_process_batch_dockerfile_in_one_struct(self):
    #     project_path = "./example"
    #     build_ctx = "/home/haoside/Desktop/aaa"
    #
    #     for filename in os.listdir(project_path):
    #         file_path = os.path.join(project_path, filename)
    #         try:
    #             print(filename)
    #             dockerfile_meta: Optional[DockerfileMeta] = process(file_path, build_ctx)
    #         except Exception:
    #             raise
