import logging
import os
import sys
import unittest
from concurrent.futures import ThreadPoolExecutor

from graphgen.config.definitions import ROOT_DIR
from graphgen.graph.Entity.EntityNode import *
from graphparse.datatypes.tool_graph import ToolGraph, make_tool_graph
from graphparse.neo4j_reader.neo4j_reader import Neo4jConnection

LOG_PATH = f"{ROOT_DIR}/../logs/script_build.log"
# 创建日志
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(filename=LOG_PATH, encoding='utf-8')
formatter = logging.Formatter('[{levelname}:{asctime}:{module}:{funcName}:{lineno}] {message}', style='{')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


class TestToolGraph(unittest.TestCase):
    def test_too_graph_gen(self):
        key_word = "go"
        conn = Neo4jConnection()
        all_tool_pkg_node_name = conn.get_all_tool_pkg_node_name()
        for tool_pkg_name in all_tool_pkg_node_name:
            if key_word in tool_pkg_name:
                print(f"====================================={tool_pkg_name}====================================")
                tool_pkg_node: ToolPkgNode = conn.get_tool_pkg_node_by_name(tool_pkg_name)
                dependencies = conn.get_single_tool_pkg_node_real_step(tool_pkg_name)
                tool_graph: ToolGraph = make_tool_graph(tool_pkg_name, tool_pkg_node.url, dependencies)
                print(tool_graph.gen_install_script())

        conn.close()


class TestBatchScriptToBuildGraph(unittest.TestCase):
    def test_single_script(self):
        filename = "bartixxx32___hidden-eye###174526###4d82cb4515b4d36cb9080f7c76df076ca0580910_script.cypher"
        script_path = f"/home/haoside/Desktop/output/{filename}"
        conn = Neo4jConnection()
        with open(script_path, "r") as file:
            cypher_script = file.read()
        conn.run_script(cypher_script)
        conn.close()

    def test_re_run_single_script(self):
        conn = Neo4jConnection()
        with open(f"{ROOT_DIR}/../logs/error_build.log", "r") as file:
            for line in file.readlines():
                try:
                    filename = line.replace("脚本构建错误！", "").strip()
                    script_path = f"/home/haoside/Desktop/output/{filename}"
                    with open(script_path, "r") as file:
                        cypher_script = file.read()
                        conn.run_script(cypher_script)
                except Exception as e:
                    with open(f"{ROOT_DIR}/../logs/error_build2.log", "a") as f:
                        f.write(f"{filename}脚本重新运行错误！\n")
        conn.close()

    # def test_batch_script_to_build_graph(self):
    #     script_dir_path = "/home/haoside/Desktop/output"
    #     conn = Neo4jConnection()
    #
    #     cnt = 1
    #     for file_name in os.listdir(script_dir_path):
    #         try:
    #             if cnt % 500 == 0:
    #                 print(f"{cnt}个脚本已处理！")
    #             if file_name.endswith(".cypher"):
    #                 script_path = os.path.join(script_dir_path, file_name)
    #                 with open(script_path, "r") as file:
    #                     cypher_script = file.read()
    #                 conn.run_script(cypher_script)
    #                 cnt += 1
    #         except Exception as e:
    #             print(f"{file_name}脚本构建错误！", file=sys.stderr)
    #
    #     conn.close()

    @staticmethod
    def process_cypher_script(script_dir_path, file_name, conn):
        script_path = os.path.join(script_dir_path, file_name)
        try:
            with open(script_path, "r") as file:
                cypher_script = file.read()
            if cypher_script:
                conn.run_script(cypher_script)

            logging.info(f"成功处理脚本: {file_name}")
        except Exception as e:
            logging.error(f"处理文件 {file_name} 时出错: {e}", exc_info=True)

    def test_batch_script_to_build_graph(self):
        script_dir_path = "/home/haoside/Desktop/output"

        cnt = 0
        # 要求以.cypher结尾
        cypher_files = [file_name for file_name in os.listdir(script_dir_path) if file_name.endswith(".cypher")]

        with Neo4jConnection() as conn:
            with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
                for file_name in cypher_files:
                    cnt += 1
                    if cnt % 500 == 0:
                        logging.info(f"{cnt}个脚本已处理！")
                    executor.submit(self.process_cypher_script, script_dir_path, file_name, conn)
