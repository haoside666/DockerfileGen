from abc import ABC, abstractmethod
from collections import OrderedDict, defaultdict, deque
from typing import List

from graphparse.datatypes.demand import Demand
from graphgen.graph.Entity.EntityNode import EntityNode, SinglePkgNode, BootNode, OtherNode


class SolveInterface(ABC):
    def __init__(self, demand: Demand) -> None:
        self.demand: Demand = demand

    @abstractmethod
    def type_solver(self) -> str:
        pass

    # 优化结点列表
    def gen_text_by_entity_node_list(self, entity_node_list) -> str:
        content = ""
        single_node_info_list = []
        blocks = []
        config_nodes = []
        for item in entity_node_list:
            if isinstance(item, List):
                if isinstance(item[0], SinglePkgNode):
                    all_single_pkg_info = []
                    for entity_node in item:
                        pkg_info = entity_node.optimize()
                        if pkg_info not in all_single_pkg_info:
                            all_single_pkg_info.append(pkg_info)
                    single_node_info_list.append(all_single_pkg_info)
                # ToolPkg形式
                else:
                    lines = []
                    for entity_node in item:
                        if isinstance(entity_node, BootNode) or isinstance(entity_node, OtherNode):
                            config_nodes.append(entity_node)
                        else:
                            lines.append(entity_node.pretty())

                    # 处理block_text
                    blocks.append("\n".join(self.process_tool_pkg_block(lines)) + "\n")

            elif isinstance(item, EntityNode):
                content += item.pretty() + "\n"

        # 处理单包结点
        content += self.handle_single_node(single_node_info_list)
        # 处理工具包结点
        content += "".join(blocks)
        # 处理配置结点
        content += self.handle_config_node(config_nodes)
        return content

    def handle_single_node(self, single_node_info_list) -> str:
        result = ""
        # 处理单包结点
        # 如果method 和 flag 和 cmd_operand_list相同可以合并
        # 合并操作的结果保持顺序
        sorted_keys, key_map = self.get_single_pkg_order(single_node_info_list)
        merged_dict = dict()

        # 遍历拓扑排序后的顺序并合并
        for key in sorted_keys:
            values = key_map[key]
            if values:
                # 获取第一部分较长的值
                first_part = max([v[0] for v in values], key=len)

                # 合并第二部分，去重后连接
                second_part = " ".join(sorted(set(" ".join(v[1].split()) for v in values)))

                merged_dict[key] = (first_part, second_part)

        # 输出最终合并结果
        for key, value in merged_dict.items():
            result += f"RUN {key} {value[0]} {value[1]}".strip() + "\n"

        return result

    def handle_config_node(self, config_nodes):
        config_dict = dict()
        for config_node in config_nodes:
            node_name = config_node.name
            if node_name not in config_dict:
                config_dict[node_name] = config_node
            else:
                if config_node.weight_value > config_dict[node_name].weight_value:
                    config_dict[node_name] = config_node

        return "\n".join([node.pretty() for node in config_dict.values()])

    @staticmethod
    # 保留单包结点前后顺序
    def get_single_pkg_order(lists):
        # 构建有向图和入度表
        graph = defaultdict(list)  # 存储图的邻接表
        in_degree = defaultdict(int)  # 存储每个节点的入度
        key_map = defaultdict(list)  # 存储每个key对应的值（值为元组）

        # 构建图的结构
        for sublist in lists:
            for key, value in sublist:
                key_map[key].append(value)  # 记录每个key对应的值
                if key not in in_degree:  # 初始化入度为0的key
                    in_degree[key] = 0

        # 创建依赖关系（有向边）
        for sublist in lists:
            for i in range(len(sublist) - 1):
                key1, _ = sublist[i]
                key2, _ = sublist[i + 1]
                if key2 not in graph[key1]:
                    graph[key1].append(key2)
                    in_degree[key2] += 1

        # 执行拓扑排序
        sorted_keys = topological_sort(graph, in_degree)
        return sorted_keys, key_map

    @staticmethod
    def process_tool_pkg_block(dockerfile_lines):
        processed_lines = []
        combined_command = []

        for line in dockerfile_lines:
            line = line.strip()
            if line.startswith('RUN'):
                command = line[4:].strip()
                combined_command.append(command)
            else:
                if combined_command:
                    processed_lines.append('RUN ' + ' && \\\n    '.join(combined_command))
                    combined_command = []
                processed_lines.append(line)

        if combined_command:
            processed_lines.append('RUN ' + ' && \\\n    '.join(combined_command))

        return processed_lines


# Kahn 算法进行拓扑排序
def topological_sort(graph, in_degree):
    queue = deque([node for node in in_degree if in_degree[node] == 0])
    result = []

    while queue:
        node = queue.popleft()
        result.append(node)

        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    # 检查是否有环
    if len(result) == len(in_degree):
        return result
    else:
        return None
