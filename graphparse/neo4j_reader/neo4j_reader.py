from typing import List

from graphgen.config.definitions import ROOT_DIR
from graphgen.config.db_config import *

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

    def clear(self):
        try:
            with self.driver.session() as session:
                # 执行Cypher查询以清空数据库
                session.run("MATCH (n) DETACH DELETE n")
            print("Database cleared successfully.")
        except Exception as e:
            print(f"An error occurred while clearing the database: {e}")

    # 为所有结点添加权重属性
    def add_weight_to_graph(self, weight_info):
        try:
            with self.driver.session() as session:
                for hash_value, weight_value in weight_info:
                    try:
                        session.run(
                            "MATCH (n) WHERE n.hash_value = $hash_value SET n.weight_value = $weight_value",
                            hash_value=hash_value,
                            weight_value=weight_value
                        )
                    except Exception as e:
                        print(f"An error occurred while adding weight to node with hash_value {hash_value}: {e}")
                        continue
        except Exception as e:
            print(f"An error occurred during the session: {e}")

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

    def get_single_tool_pkg_node_real_step(self, tool_pkg_name: str) -> List[Tuple[Tuple, Tuple]]:
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

    # # 通过镜像名获取所有镜像结点哈希值
    # def get_all_image_node_hash_value_by_image_name(self, image_name) -> List[str]:
    #     with self.driver.session() as session:
    #         result = session.run("MATCH (n:Image {name: $name}) RETURN n", name=image_name)
    #         data = result.data()
    #         hash_values = []
    #         for item in data:
    #             hash_values.append(item['n']['hash_value'])
    #         return hash_values

    # 通过hash_value获取结点信息
    def get_node_by_hash_value(self, hash_value) -> EntityNode:
        with self.driver.session() as session:
            result = session.run(
                "MATCH (n) WHERE n.hash_value = $hash_value RETURN n,labels(n) AS label_name",
                hash_value=hash_value
            )
            data = result.data()
            assert len(data) == 1
            property_dict = data[0]['n']
            label = data[0]['label_name']
            entity_node = gen_entity_node_by_label_and_property(label[0], property_dict)
            return entity_node

    # 通过镜像名获取权重值最大的镜像结点
    def get_max_weight_image_node_by_image_name(self, image_name) -> Optional[EntityNode]:
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (n:Image {name: $name})
                RETURN n, n.weight_value
                ORDER BY n.weight_value DESC
                LIMIT 1
                """,
                name=image_name
            )
            data = result.data()
            if len(data) == 0:
                return None
            property_dict = data[0]['n']
            entity_node = gen_entity_node_by_label_and_property("Image", property_dict)
            return entity_node

    def get_image_node_by_image_name_and_version(self, image_name, image_version) -> Optional[EntityNode]:
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (n:Image {name: $name,tag: $version})   
                RETURN n
                LIMIT 1
                """,
                name=image_name,
                version=image_version
            )
            data = result.data()
            if len(data) == 0:
                return None
            property_dict = data[0]['n']
            entity_node = gen_entity_node_by_label_and_property("Image", property_dict)
            return entity_node

    # 根据基础镜像获取文件系统包
    def get_file_pkg_by_base_image(self, hash_value: str) -> Optional[EntityNode]:
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (base:Image {hash_value: $hash_value})-[:Exist]->(fp:FilePkg)
                RETURN fp
                ORDER BY fp.weight_value DESC
                LIMIT 1
                """,
                hash_value=hash_value
            )
            data = result.data()
            if len(data) == 0:
                return None
            property_dict = data[0]['fp']
            entity_node = gen_entity_node_by_label_and_property("FilePkg", property_dict)
            return entity_node

    def get_dependency_node_list_of_file_pkg(self, hash_value: str) -> Optional[List[EntityNode]]:
        dependency_node_list = []
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (base:FilePkg {hash_value: $hash_value})-[:Dependency]-> (s:Step)
                RETURN s
                """,
                hash_value=hash_value
            )
            data = result.data()
            if len(data) == 0:
                return dependency_node_list
            dependency_info_dict = {}
            for idx, record in enumerate(data):
                s = record['s']
                name = s["name"]
                if name in dependency_info_dict:
                    if dependency_info_dict[name][0] < s['weight_value']:
                        dependency_info_dict[name] = (s['weight_value'], idx)
                else:
                    dependency_info_dict[name] = (s['weight_value'], idx)
            for name, info in dependency_info_dict.items():
                property_dict = data[info[1]]['s']
                entity_node = gen_entity_node_by_label_and_property("Step", property_dict)
                dependency_node_list.append(entity_node)
            return dependency_node_list

    def get_config_node_list_of_file_pkg(self, hash_value: str) -> Optional[List[EntityNode]]:
        config_node_list = []
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (base:FilePkg {hash_value: $hash_value})-[:Settings]-> (c:Config)
                RETURN c
                """,
                hash_value=hash_value
            )
            data = result.data()
            if len(data) == 0:
                return config_node_list
            config_info_dict = {}
            for idx, record in enumerate(data):
                s = record['c']
                name = s["name"]
                if "weight_value" in s:
                    if name in config_info_dict:
                        if config_info_dict[name][0] < s['weight_value']:
                            config_info_dict[name] = (s['weight_value'], idx)
                    else:
                        config_info_dict[name] = (s['weight_value'], idx)
            for name, info in config_info_dict.items():
                property_dict = data[info[1]]['c']
                entity_node = gen_entity_node_by_label_and_property("Config", property_dict)
                config_node_list.append(entity_node)
            priority = {
                "EXPOSE": 0,  # EXPOSE 优先级最高
                "ENTRYPOINT": 1,  # ENTRYPOINT 排第二
                "CMD": 2  # CMD 排最后
            }

            # 使用 sorted 函数并按照优先级排序
            sorted_config_node_list = sorted(config_node_list, key=lambda x: priority[x.name])
            return sorted_config_node_list

    def run_script(self, script):
        with self.driver.session() as session:
            session.run(script)

# if __name__ == "__main__":
#     key_word = "hdf5"
#     conn = Neo4jConnection()
#     all_tool_pkg_node_name = conn.get_all_tool_pkg_node_name()
#     all_tool_pkg_graph = []
#     for tool_pkg_name in all_tool_pkg_node_name:
#         if key_word in tool_pkg_name:
#             # conn.get_single_tool_pkg_node_all_has_relation(tool_pkg_name)
#             dependencies = conn.get_single_tool_pkg_node_real_step(tool_pkg_name)
#             for dep in dependencies:
#                 print(f"{dep[0]} dependency {dep[1]}")
#
#     conn.close()
