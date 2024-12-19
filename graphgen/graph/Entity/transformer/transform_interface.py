from abc import ABC, abstractmethod
from graphgen.dockerfile_process.preprocess.datatypes.PrimitiveMeta import PrimitiveMeta
from typing import Tuple, Set, Optional
from graphgen.graph.Entity.EntityNode import EntityNode


class TransformInterface(ABC):
    def __init__(self, p_meta: PrimitiveMeta) -> None:
        self.p_meta: PrimitiveMeta = p_meta

    @abstractmethod
    def transform(self) -> EntityNode:
        pass
