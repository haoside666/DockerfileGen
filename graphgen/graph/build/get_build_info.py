from typing import List, Optional, Union

from graphgen.dependency.datatypes.DDType import DDType
from graphgen.dependency.datatypes.EdgeIndexList import EdgeIndexList

from graphgen.graph.Entity.EntityNode import *
from graphgen.graph.build.datatypes.RType import RType
from graphgen.graph.build.datatypes.Relation import Relation
from graphgen.graph.build.datatypes.RelationList import RelationList, make_relation_list_from_image_and_execute_node


def strip_redundant_node(entity_list: List[EntityNode]):
    new_entity_list: List[EntityNode] = []
    for entity_node in entity_list:
        if isinstance(entity_node, DefaultNode) or isinstance(entity_node, BootNode) \
                or isinstance(entity_node, ArgNode) or isinstance(entity_node, EnvNode):
            continue
        else:
            new_entity_list.append(entity_node)
    return new_entity_list


# 生成基础镜像与可执行命令节点
# def generate_base_image_and_execute_node(entity_list: List[EntityNode]) -> Tuple[Optional[ImageNode], List[ExecutableNode]]:
#     img_node = None
#     exe_cmd_node_list = []
#     cmd_set = set()
#     pkg_set = set()
#     pkg_cmd_set = set()
#     for entity_node in entity_list:
#         if isinstance(entity_node, CommandNode):
#             for cmd in entity_node.cmd_set:
#                 cmd_set.add(cmd)
#         elif isinstance(entity_node, PkgNode):
#             pkg_cmd = entity_node.name
#             pkg_cmd_set.add(pkg_cmd)
#             current_pkg_list = entity_node.pkg_list
#             if pkg_cmd not in current_pkg_list:
#                 cmd_set.add(pkg_cmd)
#                 pkg_set = pkg_set.union(set(current_pkg_list))
#             else:
#                 cmd_set = cmd_set.union(set(current_pkg_list))
#         elif isinstance(entity_node, ImageNode):
#             img_node = entity_node
#     diff_set = cmd_set - pkg_set
#     for cmd in diff_set:
#         if cmd in pkg_cmd_set:
#             exe_cmd_node_list.append(ExecutableNode(cmd, "pkg"))
#         else:
#             exe_cmd_node_list.append(ExecutableNode(cmd))
#     return img_node, exe_cmd_node_list

# 生成基础镜像与可执行命令节点
def generate_base_image_and_execute_node(entity_list: List[EntityNode], edge_index_list: EdgeIndexList) -> Tuple[Optional[ImageNode], List[ExecutableNode]]:
    img_node = None
    exe_cmd_node_list = []
    cmd_set = set()
    pkg_cmd_set = set()
    pkg_index_list = find_all_pkg_dependency(entity_list, edge_index_list)
    for idx, entity_node in enumerate(entity_list):
        if idx in pkg_index_list:
            continue
        if isinstance(entity_node, CommandNode):
            for cmd in entity_node.cmd_list:
                cmd_set.add(cmd)
        elif isinstance(entity_node, PkgNode):
            pkg_cmd = entity_node.name
            if pkg_cmd not in entity_node.pkg_list:
                cmd_set.add(pkg_cmd)
                pkg_cmd_set = pkg_cmd_set.union(set(entity_node.pkg_list))
            else:
                cmd_set = cmd_set.union(set(entity_node.pkg_list))
        elif isinstance(entity_node, ImageNode):
            img_node = entity_node
    for cmd in cmd_set:
        if cmd in pkg_cmd_set:
            exe_cmd_node_list.append(ExecutableNode(cmd, "pkg"))
        else:
            exe_cmd_node_list.append(ExecutableNode(cmd))
    return img_node, exe_cmd_node_list


# 生成可执行文件节点和包结点节点
def generate_pkg_node_and_cmd_node(entity_list: List[EntityNode], exe_cmd_node_list: List[ExecutableNode]) -> RelationList:
    r_list: RelationList = RelationList()
    all_pkg_node_list: List[SinglePkgNode] = []
    for entity_node in entity_list:
        if isinstance(entity_node, PkgNode):
            pkg_name = entity_node.name
            dest_node: Union[ExecutableNode, SinglePkgNode] = find_exe_cmd_node(pkg_name, exe_cmd_node_list)
            if dest_node is None:
                dest_node = find_pkg_node(pkg_name, all_pkg_node_list)
                if dest_node is None:
                    raise Exception("pkg node not found")
            pkg_node_list: list[SinglePkgNode] = entity_node.split()
            for pkg_node in pkg_node_list:
                if pkg_node not in all_pkg_node_list:
                    all_pkg_node_list.append(pkg_node)

                if pkg_node != dest_node:
                    r: Relation = Relation(pkg_node, dest_node, RType.Dependency)
                    r_list.add_relation(r)
    return r_list


# 生成工具包节点
# 寻找命令结点中类型为url的节点
def generate_tool_node(entity_list: List[EntityNode], edge_index_list: EdgeIndexList) -> RelationList:
    r_list: RelationList = RelationList()
    url_node_list: List[CommandNode] = []
    for idx, entity_node in enumerate(entity_list):
        if isinstance(entity_node, CommandNode) and entity_node.cmd_type == "url":
            url_node_list.append(entity_node)
    if url_node_list:
        pass
    return r_list


def find_exe_cmd_node(pkg_name: str, exe_cmd_node_list: List[ExecutableNode]) -> Optional[ExecutableNode]:
    for exe_cmd_node in exe_cmd_node_list:
        if exe_cmd_node.name == pkg_name:
            return exe_cmd_node
    return None


def find_pkg_node(pkg_name: str, all_pkg_node_set: List[SinglePkgNode]) -> Optional[SinglePkgNode]:
    for pkg_cmd_node in all_pkg_node_set:
        if pkg_name == pkg_cmd_node.name:
            return pkg_cmd_node
    return None


def find_all_pkg_dependency(entity_list: List[EntityNode], edge_index_list: EdgeIndexList) -> List[int]:
    pkg_index_list: List[int] = []
    for idx, d_type in enumerate(edge_index_list.type_list):
        if d_type == DDType.RUN_PKG:
            before_node = entity_list[edge_index_list.edge_index_list[idx][0]]
            dependency_pkg_idx = edge_index_list.edge_index_list[idx][1]
            after_node = entity_list[dependency_pkg_idx]
            if before_node.name != after_node.name:
                pkg_index_list.append(dependency_pkg_idx)

    return pkg_index_list
