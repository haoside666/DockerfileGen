from typing import List

from dockdepend.util import standard_repr, standard_eq
from dockdepend.dockerfile_process.datatypes.PrimitiveMetaList import PrimitiveMetaList


class DockerfilePrimitiveMeta:
    def __init__(self, is_mutil_stage: bool = False) -> None:
        self.stage_meta_list: List[PrimitiveMetaList] = []
        self.is_mutil_stage: bool = is_mutil_stage

    def add_element_to_stage_meta_list(self, p_meta_list: PrimitiveMetaList) -> None:
        self.stage_meta_list.append(p_meta_list)

    def __repr__(self):
        return standard_repr(self)

    def __eq__(self, other) -> bool:
        return standard_eq(self, other)
