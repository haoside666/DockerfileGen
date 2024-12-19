from typing import List, Optional

from graphgen.dependency.datatypes.EdgeIndexList import EdgeIndexList

from graphgen.graph.Entity.EntityNode import *
from graphgen.graph.build.datatypes.ExcuteCmdNode import ExecutableNode


# 生成基础镜像与可执行命令节点
def generate_base_image_node_and_cmd_node(entity_list: List[EntityNode]) -> Tuple[Optional[ImageNode], List[ExecutableNode]]:
    img_node = None
    exe_cmd_node_list = []
    for entity_node in entity_list:
        if isinstance(entity_node, ImageNode):
            img_node = entity_node
        elif isinstance(entity_node, CommandNode):
            pass

    return img_node, exe_cmd_node_list


# 生成可执行文件节点和包结点节点
def generate_pkg_node_and_cmd_node(entity_list: List[EntityNode]):
    pass


# 生成工具包节点
def generate_tool_node(entity_list: List[EntityNode]):
    pass
