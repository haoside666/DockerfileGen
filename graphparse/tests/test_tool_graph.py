import unittest

from graphgen.graph.Entity.EntityNode import *
from graphparse.datatypes.tool_graph import ToolGraph, make_tool_graph
from graphparse.neo4j_reader.neo4j_reader import Neo4jConnection


class TestToolGraph(unittest.TestCase):
    def test_too_graph_gen(self):
        key_word = "hdf5"
        conn = Neo4jConnection()
        all_tool_pkg_node_name = conn.get_all_tool_pkg_node_name()
        for tool_pkg_name in all_tool_pkg_node_name:
            if key_word in tool_pkg_name:
                tool_pkg_node: ToolPkgNode = conn.get_tool_pkg_node_by_name(tool_pkg_name)
                dependencies = conn.get_single_tool_pkg_node_real_step(tool_pkg_name)
                tool_graph: ToolGraph = make_tool_graph(tool_pkg_name, tool_pkg_node.url, dependencies)
                print(tool_graph.gen_install_script())
        conn.close()
