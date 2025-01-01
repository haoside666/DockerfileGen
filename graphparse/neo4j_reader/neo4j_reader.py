from typing import List

from graphgen.config.definitions import ROOT_DIR
from graphgen.config.neo4j_config import *

from neo4j import GraphDatabase

from graphgen.graph.Entity.EntityNode import *


class Neo4jConnection:
    def __init__(self):
        self.driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PWD))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        self.driver.close()

    def get_all_tool_pkg_node_name(self) -> List[str]:
        with self.driver.session() as session:
            result = session.run("MATCH (n:ToolPkg) RETURN n")
            data = result.data()
            name_list = []
            for item in data:
                name_list.append(item['n']['name'])
            return name_list

    def get_tool_pkg_node_by_name(self, tool_pkg_name: str):
        with self.driver.session() as session:
            result = session.run(
                "MATCH (n:ToolPkg {name: $name}) RETURN n",
                name=tool_pkg_name
            )
            data = result.data()
            if len(data) == 0:
                return None
            tool_pkg_node = gen_entity_node_by_label_and_property("ToolPkg", data[0]['n'])
            return tool_pkg_node

    def get_single_tool_pkg_node_all_has_relation(self, tool_pkg_name: str):
        with self.driver.session() as session:
            result = session.run(
                "MATCH (:ToolPkg {name: $name})-[:Has]-(m) RETURN m",
                name=tool_pkg_name
            )
            data = result.data()
            return data

    def get_single_tool_pkg_node_real_step(self, tool_pkg_name: str):
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (pkg:ToolPkg {name: $name})-[:Has]->(s1)
                MATCH (s1)-[:Dependency]->(s2)
                  WHERE (pkg)-[:Has]->(s2)
                RETURN DISTINCT s1, s2, labels(s1) AS s1_labels, labels(s2) AS s2_labels;
                """,
                name=tool_pkg_name
            )
            data = result.data()
            relations = []
            for record in data:
                s1 = record['s1']  # 获取 s1 的 ID
                s2 = record['s2']  # 获取 s2 的 ID
                s1_labels = record['s1_labels']
                s2_labels = record['s2_labels']
                relations.append(((s1_labels, s1), (s2_labels, s2)))

            return relations

    def run_script(self, script):
        with self.driver.session() as session:
            session.run(script)


if __name__ == "__main__":
    key_word = "hdf5"
    conn = Neo4jConnection()
    all_tool_pkg_node_name = conn.get_all_tool_pkg_node_name()
    all_tool_pkg_graph = []
    for tool_pkg_name in all_tool_pkg_node_name:
        if key_word in tool_pkg_name:
            # conn.get_single_tool_pkg_node_all_has_relation(tool_pkg_name)
            dependencies = conn.get_single_tool_pkg_node_real_step(tool_pkg_name)
            for dep in dependencies:
                print(f"{dep[0]} dependency {dep[1]}")

    conn.close()
