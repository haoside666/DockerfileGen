from typing import List

from graphgen.config.definitions import ROOT_DIR
from graphgen.graph.Entity.EntityNode import *
from graphgen.graph.builds.datatypes.RType import RType
from graphgen.graph.builds.datatypes.Relation import Relation
from graphgen.util import return_empty_list_if_none_else_itself, standard_repr, standard_eq


class RelationList:
    def __init__(self, relation_list: List[Relation] = None) -> None:
        self.relation_list: List[Relation] = return_empty_list_if_none_else_itself(relation_list)

    def __repr__(self):
        return standard_repr(self)

    def __eq__(self, other) -> bool:
        return standard_eq(self, other)

    def __str__(self) -> str:
        content = ""
        for r in self.relation_list:
            content += f"{r.entity1} -{r.relation_type}-> {r.entity2}\n"
        return content

    def add_relation(self, relation: Relation) -> None:
        if relation not in self.relation_list:
            self.relation_list.append(relation)

    def __add__(self, other):
        return RelationList(self.relation_list + other.relation_list)

    def union(self, other: 'RelationList') -> 'RelationList':
        return RelationList(self.relation_list + other.relation_list)

    # 生成neo4j脚本
    def gen_neo4j_script(self) -> str:
        entities = {}
        cypher_statements = []

        for relation in self.relation_list:
            entity1, entity2, relation_type = relation.entity1, relation.entity2, relation.relation_type

            # 处理第一个实体
            hash_val1 = entity1.calc_hash()
            if hash_val1 not in entities:
                entities[hash_val1] = f"{hash_val1}{entity1.get_entity_create_script()}"
                cypher_statements.append(f"MERGE ({entities[hash_val1]})")

            # 处理第二个实体
            hash_val2 = entity2.calc_hash()
            if hash_val2 not in entities:
                entities[hash_val2] = f"{hash_val2}{entity2.get_entity_create_script()}"
                cypher_statements.append(f"MERGE ({entities[hash_val2]})")

            # 添加关系
            cypher_statements.append(f"MERGE ({hash_val1})-[:{relation_type.name}]->({hash_val2})")

        return "\n".join(cypher_statements)

    @staticmethod
    def add_constraint() -> str:
        # with open(f"{ROOT_DIR}/graph/Entity/EntityNode.py") as file:
        #     pattern = r"class (.*?)\(EntityNode\):\s+NodeName = '(.*?)'\s"
        #     re.findall(r"pattern", file.read())
        # 预执行一遍即可
        constraint_list = [
            "CREATE CONSTRAINT constraints_Image FOR (p:Image) REQUIRE (p.name, p.tag) IS UNIQUE;"
            "CREATE CONSTRAINT constraints_ExeCmd FOR (p:ExeCmd) REQUIRE (p.name, p.type) IS UNIQUE;"
            "CREATE CONSTRAINT constraints_Cmd FOR (p:Cmd) REQUIRE p.value IS UNIQUE;"
            "CREATE CONSTRAINT constraints_ToolPkg FOR (p:ToolPkg) REQUIRE (p.url, p.cmd_list) IS UNIQUE;"
            "CREATE CONSTRAINT constraints_Pkg FOR (p:Pkg) REQUIRE (p.name, p.version, p.flags, p.cmd_flag_list, p.cmd_operand_list) IS UNIQUE;"
            "CREATE CONSTRAINT constraints_PkgCmd FOR (p:PkgCmd) REQUIRE (p.name, p.flags, p.cmd_flag_list, p.cmd_operand_list) IS UNIQUE;"
            "CREATE CONSTRAINT constraints_Boot FOR (p:Boot) REQUIRE (p.name, p.flags, p.value) IS UNIQUE;"
            "CREATE CONSTRAINT constraints_Env FOR (p:Env) REQUIRE (p.name, p.flags, p.value) IS UNIQUE;"
            "CREATE CONSTRAINT constraints_Arg FOR (p:Arg) REQUIRE (p.name, p.flags, p.value) IS UNIQUE;"
            "CREATE CONSTRAINT constraints_File FOR (p:File) REQUIRE (p.name, p.flags, p.src, p.dest) IS UNIQUE;"
            "CREATE CONSTRAINT constraints_OTHER FOR (p:OTHER) REQUIRE (p.name, p.flags, p.value) IS UNIQUE;"
        ]
        return "\n".join(constraint_list) + "\n"


def make_relation_list_from_image_and_execute_node(img_node: EntityNode, execute_node_list: List[EntityNode]) -> RelationList:
    r_list: RelationList = RelationList()
    if img_node is None:
        return r_list
    for exe_node in execute_node_list:
        r_list.relation_list.append(Relation(img_node, exe_node, RType.Contain))
        r_list.relation_list.append(Relation(exe_node, img_node, RType.Compatible))

    return r_list
