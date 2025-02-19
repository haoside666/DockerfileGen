import heapq
from collections import defaultdict
from typing import List, Tuple, Dict

from graphgen.graph.Entity.EntityNode import *
from graphgen.util import standard_repr, standard_eq


class ToolGraph:
    def __init__(self, name: str, url: str, entity_node_list: List[EntityNode], edge_list: List, weight_list: List = None):
        self.name: str = name
        self.url: str = url
        self.entity_node_list: List[EntityNode] = entity_node_list
        self.edge_list: List[Tuple[int, int]] = edge_list  # 前一个节点依赖于后一个节点
        self.weight_list: List[int] = [1] * len(self.entity_node_list) if weight_list is None else weight_list  # 权重列表

    def __repr__(self):
        return standard_repr(self)

    def __eq__(self, other) -> bool:
        return standard_eq(self, other)

    # 采用带权值的拓扑排序算法生成包安装文本
    def gen_install_step(self) -> List[EntityNode]:
        # install_script: str = ""

        graph = defaultdict(list)
        in_degree = defaultdict(int)
        # d_src->d_dst 表示依赖源依赖于依赖目标
        for d_src_index, d_dst_index in self.edge_list:
            graph[d_dst_index].append(d_src_index)  # 键: 依赖目标节点 值: 所有依赖于该目标节点的源节点
            in_degree[d_src_index] += 1

        # 初始化优先队列，按权重从大到小排序（用负数表示大根堆）
        priority_queue = []
        for node_index, entity_node in enumerate(self.entity_node_list):
            if in_degree[node_index] == 0:
                heapq.heappush(priority_queue, (-self.weight_list[node_index], node_index))

        # 拓扑排序
        topological_order = []
        while priority_queue:
            _, node_index = heapq.heappop(priority_queue)  # 取出权重最大的节点
            topological_order.append((node_index, self.weight_list[node_index]))
            for neighbor_index in graph[node_index]:
                in_degree[neighbor_index] -= 1
                if in_degree[neighbor_index] == 0:
                    heapq.heappush(priority_queue, (-self.weight_list[neighbor_index], neighbor_index))
        # 根据拓扑排序结果生成安装文本
        order_entity_list = [self.entity_node_list[node_index] for node_index, weight in topological_order]
        # for entity_node in order_entity_list:
        #     install_script += entity_node.pretty() + "\n"
        return order_entity_list

    def gen_config_info(self):
        pass


def make_tool_graph(name: str, url: str, relations: List[Tuple[Tuple, Tuple]]) -> ToolGraph:
    entity_node_list: List[EntityNode] = []
    edge_list: List = []

    for entity1_info, entity2_info in relations:
        label1, property1 = entity1_info
        label2, property2 = entity2_info
        entity1: EntityNode = gen_entity_node_by_label_and_property(label1[0], property1)
        entity2: EntityNode = gen_entity_node_by_label_and_property(label2[0], property2)
        if entity1 not in entity_node_list:
            entity_node_list.append(entity1)
        if entity2 not in entity_node_list:
            entity_node_list.append(entity2)
        index1 = entity_node_list.index(entity1)
        index2 = entity_node_list.index(entity2)
        edge_list.append((index1, index2))
    return ToolGraph(name, url, entity_node_list, edge_list)
