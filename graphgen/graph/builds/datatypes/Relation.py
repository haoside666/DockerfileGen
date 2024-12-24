from graphgen.graph.Entity.EntityNode import EntityNode
from graphgen.graph.builds.datatypes.RType import RType
from graphgen.util import standard_repr, standard_eq


class Relation:

    def __init__(self, entity1: EntityNode, entity2: EntityNode, relation_type: RType) -> None:
        self.entity1: EntityNode = entity1
        self.entity2: EntityNode = entity2
        self.relation_type: RType = relation_type

    def __repr__(self):
        return standard_repr(self)

    def __eq__(self, other) -> bool:
        return standard_eq(self, other)

    # # CREATE (a:EntityA {name: 'EntityA_Name'})-[r:RELATIONSHIP_TYPE]->(b:EntityB {name: 'EntityB_Name'})
    # def get_neo4j_entity_create_script(self) -> str:
    #     return f"CREATE ({self.entity1.get_entity_create_script()})-[r:{self.relation_type.name}]->({self.entity2.get_entity_create_script()})"
