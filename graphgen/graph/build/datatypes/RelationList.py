from typing import List

from graphgen.graph.Entity.EntityNode import *
from graphgen.graph.build.datatypes.RType import RType
from graphgen.graph.build.datatypes.Relation import Relation
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

    # 生成neo4j脚本
    def gen_neo4j_script(self) -> str:
        content = ""
        for r in self.relation_list:
            content += f"{r.get_neo4j_entity_create_script()}\n"
        return content


def make_relation_list_from_image_and_execute_node(img_node: EntityNode, execute_node_list: List[EntityNode]) -> RelationList:
    r_list: RelationList = RelationList()
    if img_node is None:
        return r_list
    for exe_node in execute_node_list:
        r_list.relation_list.append(Relation(img_node, exe_node, RType.Contain))

    return r_list
