from graphgen.dependency.datatypes.DDType import DDType
from graphgen.util import standard_repr, standard_eq, return_empty_list_if_none_else_itself
from typing import List, Tuple


class EdgeIndexList:
    def __init__(self, edge_index_list: List[Tuple[int, int]] = None, type_list: List[DDType] = None,
                 msg_list: List[str] = None) -> None:
        self.edge_index_list: List[Tuple[int, int]] = return_empty_list_if_none_else_itself(edge_index_list)
        self.type_list: List[DDType] = return_empty_list_if_none_else_itself(type_list)
        self.msg_list: List[str] = return_empty_list_if_none_else_itself(msg_list)

    def __repr__(self):
        return standard_repr(self)

    def __eq__(self, other) -> bool:
        return standard_eq(self, other)

    def transform_to_list_print(self) -> List[List]:
        return [list(item) for item in self.edge_index_list]

    def pretty(self):
        new_list = [*zip(self.edge_index_list, self.msg_list)]
        s = ""
        s += '[\n'
        for edge, msg in new_list:
            edge = (edge[0] + 1, edge[1] + 1)
            s += f"\t{str(edge)},\t# {msg}\n"
        s += ']\n'
        print(s)

    def filter_list_item(self, filter_list):
        if filter_list:
            save_index = []
            for idx, dd_type in enumerate(self.type_list):
                if dd_type not in filter_list:
                    save_index.append(idx)

            edge_index_list = []
            type_list = []
            msg_list = []
            for index in save_index:
                edge_index_list.append(self.edge_index_list[index])
                type_list.append(self.type_list[index])
                msg_list.append(self.msg_list[index])
            return EdgeIndexList(edge_index_list, type_list, msg_list)
        else:
            return self

    def length(self):
        return len(self.edge_index_list)

    def add_element_to_edge_index_list(self, edge_index: Tuple[int, int], dd_type: DDType, msg: str):
        if edge_index not in self.edge_index_list:
            self.edge_index_list.append(edge_index)
            self.type_list.append(dd_type)
            self.msg_list.append(msg)

    def get_all_edge_end_index_by_start_index(self, start_index: int) -> List[int]:
        return [item[1] for item in self.edge_index_list if item[0] == start_index]


def remove_redundant_edges_in_graph(edge_index_list: EdgeIndexList) -> EdgeIndexList:
    new_edge_index_list: List[Tuple[int, int]] = []
    new_type_list: List[DDType] = []
    new_msg_list: List[str] = []
    graph = {}
    all_edge: List[Tuple[int, int]] = edge_index_list.edge_index_list
    for u, v in all_edge:
        if u not in graph:
            graph[u] = set()
        graph[u].add(v)

    edges_to_keep = set(all_edge)

    redundant_index_set = set()
    for idx, item in enumerate(all_edge):
        u, v = item
        for w in graph.get(u, []):
            if v in graph.get(w, []):
                # edges_to_keep.discard((u, v))
                redundant_index_set.add(idx)

    result = list(edges_to_keep)
    for idx in range(len(edge_index_list.edge_index_list)):
        if idx in redundant_index_set:
            continue
        new_edge_index_list.append(edge_index_list.edge_index_list[idx])
        new_type_list.append(edge_index_list.type_list[idx])
        new_msg_list.append(edge_index_list.msg_list[idx])
    return EdgeIndexList(new_edge_index_list, new_type_list, new_msg_list)
