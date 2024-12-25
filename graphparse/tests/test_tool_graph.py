import sys
import unittest
from unittest.mock import patch

from graphgen.cli import main
from graphgen.config.definitions import ROOT_DIR
from graphgen.graph.Entity.EntityNode import *
from graphparse.datatypes.tool_graph import ToolGraph, make_tool_graph
from graphparse.neo4j_reader.neo4j_reader import Neo4jConnection


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
        filename = "oberbichler___kratos-dev###1876473###bc6b211839622b3582f4d2adf19906610d4d61c4_script.cypher"
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

    def test_batch_script_to_build_graph(self):
        script_dir_path = "/home/haoside/Desktop/output"
        conn = Neo4jConnection()

        cnt = 1
        for file_name in os.listdir(script_dir_path):
            try:
                if cnt % 500 == 0:
                    print(f"{cnt}个脚本已处理！")
                if file_name.endswith(".cypher"):
                    script_path = os.path.join(script_dir_path, file_name)
                    with open(script_path, "r") as file:
                        cypher_script = file.read()
                    conn.run_script(cypher_script)
                    cnt += 1
            except Exception as e:
                print(f"{file_name}脚本构建错误！", file=sys.stderr)

        conn.close()

    # 请在此处修改文件名
    filename = "deyvisonpenha___moobitest###30081###cb0e01478aaf89b263531dbfbad9fb7b32ec477b_script.cypher"

    @patch('sys.argv',
           new=['test_cli.py', 'graph', '-f', f"/home/haoside/Desktop/input/{filename.replace('_script.cypher', '')}", '-o',
                f"/home/haoside/Desktop/output/{filename}"])
    def test_rebuild_single_script(self):
        main()
