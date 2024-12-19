from graphgen.graph.Entity.EntityNode import EntityNode
from graphgen.graph.build.datatypes.RType import RType


class Relation:

    def __init__(self, entity1: EntityNode, entity2: EntityNode, relation_type: RType) -> None:
        self.entity1: EntityNode = entity1
        self.entity2: EntityNode = entity2
        self.relation_type: RType = relation_type
