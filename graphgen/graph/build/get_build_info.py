from typing import List, Optional, Union

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
def generate_base_image_and_execute_node(entity_list: List[EntityNode]) -> Tuple[Optional[ImageNode], List[ExecutableNode]]:
    img_node = None
    exe_cmd_node_list = []
    cmd_set = set()
    pkg_set = set()
    pkg_cmd_set = set()
    for entity_node in entity_list:
        if isinstance(entity_node, CommandNode):
            for cmd in entity_node.cmd_set:
                cmd_set.add(cmd)
        elif isinstance(entity_node, PkgNode):
            pkg_cmd = entity_node.name
            pkg_cmd_set.add(pkg_cmd)
            current_pkg_set = entity_node.pkg_set
            if pkg_cmd not in current_pkg_set:
                cmd_set.add(pkg_cmd)
                pkg_set = pkg_set.union(current_pkg_set)
            else:
                cmd_set = cmd_set.union(current_pkg_set)
        elif isinstance(entity_node, ImageNode):
            img_node = entity_node
    diff_set = cmd_set - pkg_set
    for cmd in diff_set:
        if cmd in pkg_cmd_set:
            exe_cmd_node_list.append(ExecutableNode(cmd, "pkg"))
        else:
            exe_cmd_node_list.append(ExecutableNode(cmd))
    return img_node, exe_cmd_node_list


# 生成可执行文件节点和包结点节点
def generate_pkg_node_and_cmd_node(entity_list: List[EntityNode], exe_cmd_node_list: List[ExecutableNode]) -> RelationList:
    r_list: RelationList = RelationList()
    all_pkg_node_list: List[PkgNode] = []
    for entity_node in entity_list:
        if isinstance(entity_node, PkgNode):
            pkg_name = entity_node.name
            dest_node: Union[ExecutableNode, PkgNode] = find_exe_cmd_node(pkg_name, exe_cmd_node_list)
            if dest_node is None:
                dest_node = find_pkg_node(pkg_name, all_pkg_node_list)
                if dest_node is None:
                    raise Exception("pkg node not found")
            pkg_node_list: list[PkgNode] = entity_node.split()
            for pkg_node in pkg_node_list:
                if pkg_node not in all_pkg_node_list:
                    all_pkg_node_list.append(pkg_node)
            for pkg_node in pkg_node_list:
                if pkg_node != dest_node:
                    r: Relation = Relation(pkg_node, dest_node, RType.Dependency)
                    r_list.add_relation(r)
    return r_list


# 生成工具包节点
def generate_tool_node(entity_list: List[EntityNode], edge_index_list: EdgeIndexList):
    pass


def find_exe_cmd_node(pkg_name: str, exe_cmd_node_list: List[ExecutableNode]) -> Optional[ExecutableNode]:
    for exe_cmd_node in exe_cmd_node_list:
        if exe_cmd_node.cmd_name == pkg_name:
            return exe_cmd_node
    return None


def find_pkg_node(pkg_name: str, all_pkg_node_set: List[PkgNode]) -> Optional[PkgNode]:
    for pkg_cmd_node in all_pkg_node_set:
        if pkg_name in pkg_cmd_node.pkg_set:
            return pkg_cmd_node
    return None
