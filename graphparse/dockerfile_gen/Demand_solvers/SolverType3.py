from typing import List

from graphgen.graph.Entity.EntityNode import CommentNode, SinglePkgNode, ToolPkgNode
from graphparse.datatypes.tool_graph import ToolGraph, make_tool_graph
from graphparse.dockerfile_gen.Demand_solvers.solve_interface import SolveInterface
from graphparse.neo4j_reader.neo4j_reader import Neo4jConnection


# 3.只输入软件包名
#   优先查找系统包，然后查找工具包
#   对于系统包，利用深度优先搜索，寻找所有依赖的软件包，
#   对于工具包，根据软件包权重推荐软件包版本，然后在根据软件包需求命令列表筛选满足需求命令且最优的镜像
class SolverType3(SolveInterface):
    def type_solver(self) -> str:
        content = ""
        software_list = self.demand.software_list
        entity_node_list = []
        with Neo4jConnection() as conn:
            # 获取所有pkg节点
            pkg_node_list = conn.get_all_pkg_node()
            pkg_index_info = self.get_pkg_index_info(pkg_node_list)

            # 将软件包分为系统包和工具包两类
            sys_pkg_software_list = []
            tool_pkg_software_list = []
            for software in software_list:
                if ":" not in software:
                    new_software = f"{software}:latest"
                if new_software in pkg_index_info:
                    sys_pkg_software_list.append(pkg_index_info[new_software])
                else:
                    tool_pkg_software_list.append(software.split(":")[0])

            # 处理所有系统包情况
            sys_base_image_list = []
            if sys_pkg_software_list:
                sys_cmd_set = set()
                for sys_pkg_software in sys_pkg_software_list:
                    hash_value = sys_pkg_software["hash_value"]
                    dependency_chain = conn.get_pkg_node_dependency_chain(hash_value)
                    entity_node_list.append(dependency_chain)
                    sys_cmd_set.add(self.get_pkg_exe_cmd(dependency_chain))

                # 寻找符合命令集合的基础镜像列表
                sys_base_image_list = conn.find_image_list_by_cmd_list(list(sys_cmd_set))
                if not sys_base_image_list:
                    return "未找到满足条件的基础镜像!"

            # 处理所有工具包情况
            tool_base_image_list = []
            if tool_pkg_software_list:
                tool_pkg_node_name_list, tool_pkg_node_weight_list = conn.get_all_tool_pkg_node_name_and_weight_value()
                # all_tool_pkg_node = []
                tool_cmd_set = set()
                for tool_pkg_software in tool_pkg_software_list:
                    match_pkg = self.tool_pkg_similarity_match_algorithm(tool_pkg_software, tool_pkg_node_name_list, tool_pkg_node_weight_list)
                    if not match_pkg:
                        entity_node_list.append(CommentNode(f'{tool_pkg_software}生成失败!\n'))
                    else:
                        block_node_list = []
                        block_node_list.append(CommentNode(f'安装工具包{tool_pkg_software}!'))
                        # 得到工具包块信息
                        tool_pkg_node: ToolPkgNode = conn.get_tool_pkg_node_by_name(match_pkg)
                        dependencies = conn.get_single_tool_pkg_node_real_step(match_pkg)
                        tool_graph: ToolGraph = make_tool_graph(match_pkg, tool_pkg_node.url, dependencies)
                        block_node_list.extend(tool_graph.gen_install_step())
                        # 寻找所有配置结点
                        config_node_list = conn.get_config_node_list_of_tool_pkg(tool_pkg_node.hash_value)
                        block_node_list.extend(config_node_list)
                        # all_tool_pkg_node.append(tool_pkg_node)
                        tool_cmd_set = tool_cmd_set.union(set(tool_pkg_node.cmd_list))
                        entity_node_list.append(block_node_list)
                # 寻找所有工具包结点的基础镜像列表
                tool_base_image_list = conn.find_image_list_by_cmd_list(list(tool_cmd_set))
                if not tool_base_image_list:
                    return "未找到满足条件的基础镜像!"

            # 寻找基础镜像
            if sys_base_image_list and tool_base_image_list:
                common_base_image_list = list(set(sys_base_image_list) & set(tool_base_image_list))
            else:
                common_base_image_list = list(set(sys_base_image_list) | set(tool_base_image_list))
            if not common_base_image_list:
                return "未找到满足条件的基础镜像!"

            max_weight = 0
            max_index = 0
            for idx, image_node in enumerate(common_base_image_list):
                if image_node.weight_value > max_weight:
                    max_weight = image_node.weight_value
                    max_index = idx
            entity_node_list.insert(0, common_base_image_list[max_index])

        # # 优化结点信息
        # if entity_node_list:
        #     new_entity_node_list = self.optimize_node_list(entity_node_list)

        # for entity_node in entity_node_list:
        #     content += entity_node.pretty() + "\n"

        # 优化结点信息
        if entity_node_list:
            return self.gen_text_by_entity_node_list(entity_node_list)

        return content

    @staticmethod
    def get_pkg_index_info(pkg_node_list: List[SinglePkgNode]):
        pkg_index_info = {}
        for idx, pkg_node in enumerate(pkg_node_list):
            pkg_info = f'{pkg_node.name}:{pkg_node.version}'
            if pkg_info not in pkg_index_info:
                pkg_index_info[pkg_info] = {
                    "weight_value": pkg_node.weight_value,
                    "hash_value": pkg_node.hash_value,
                    "index": idx
                }
            else:
                new_weight_value = pkg_node.weight_value
                if new_weight_value > pkg_index_info[pkg_info]["weight_value"]:
                    pkg_index_info[pkg_info] = {
                        "weight_value": new_weight_value,
                        "hash_value": pkg_node.hash_value,
                        "index": idx
                    }

        return pkg_index_info

    @staticmethod
    def get_pkg_exe_cmd(dependency_chain: List[SinglePkgNode]):
        assert dependency_chain
        return dependency_chain[0].method

    @staticmethod
    # 相似度匹配算法
    def tool_pkg_similarity_match_algorithm(demand_pkg_name, tool_pkg_node_name_list, tool_pkg_node_weight_list):
        match_pkg = ""
        max_weight_value = 0
        for idx, tool_pkg_name in enumerate(tool_pkg_node_name_list):
            if demand_pkg_name in tool_pkg_name:
                if tool_pkg_node_weight_list[idx] > max_weight_value:
                    max_weight_value = tool_pkg_node_weight_list[idx]
                    match_pkg = tool_pkg_name

        return match_pkg
