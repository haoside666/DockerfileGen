from graphgen.dependency.datatypes.DDType import DDType
from graphgen.dependency.datatypes.EdgeIndexList import EdgeIndexList, remove_redundant_edges_in_graph
from graphgen.exception.CustomizedException import PkgNotFoundError

from graphgen.graph.Entity.EntityNode import *
from graphgen.graph.builds.datatypes.RType import RType
from graphgen.graph.builds.datatypes.Relation import Relation
from graphgen.graph.builds.datatypes.RelationList import RelationList


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
        if idx in pkg_index_list:  # 跳过包依赖命令
            continue
        if isinstance(entity_node, CommandNode):
            for cmd in entity_node.cmd_list:
                cmd_set.add(cmd)
        elif isinstance(entity_node, PkgNode):
            pkg_cmd = entity_node.name
            # 长度为0表示实际没有安装或处理包
            if len(entity_node.pkg_list) > 0:
                cmd_set.add(pkg_cmd)
                pkg_cmd_set = pkg_cmd_set.union(set(entity_node.pkg_list))
            else:
                cmd_set.add(pkg_cmd)
        elif isinstance(entity_node, FilePkgNode):
            cmd_set.add(entity_node.name)
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
                    raise PkgNotFoundError("pkg node not found")
            try:
                pkg_node_list: list[SinglePkgNode] = entity_node.split()
            except:
                print(f"{entity_node} split fail!")
                raise
                # return r_list
            for pkg_node in pkg_node_list:
                if pkg_node not in all_pkg_node_list:
                    all_pkg_node_list.append(pkg_node)

                if pkg_node != dest_node:
                    r: Relation = Relation(pkg_node, dest_node, RType.Dependency)
                    r_list.add_relation(r)
    return r_list


# 生成文件包结点节点,包括COPY,ADD，CMD,EXPOSE等信息
def generate_file_pkg_node(entity_list: List[EntityNode], edge_index_list: EdgeIndexList,
                           img_node: ImageNode, config_entity_list: List[ConfigNode] = None) -> RelationList:
    r_list: RelationList = RelationList()
    all_file_pkg_node_list: List[FilePkgNode] = []
    for idx, entity_node in enumerate(entity_list):
        if isinstance(entity_node, FilePkgNode):
            # 寻找文件依赖,并添加文件依赖
            dest_index_list = find_all_file_dir_dependency(idx, edge_index_list)
            for dest_index in dest_index_list:
                dest_node = entity_list[dest_index]
                step_entity_node = StepNode(dest_node)
                r: Relation = Relation(entity_node, step_entity_node, RType.Dependency)
                r_list.add_relation(r)

            # 填充文件包节点与配置信息的依赖关系
            if config_entity_list:
                for config_entity in config_entity_list:
                    r: Relation = Relation(entity_node, config_entity, RType.Settings)
                    r_list.add_relation(r)

            # 添加与基础镜像的依赖关系
            r: Relation = Relation(img_node, entity_node, RType.Exist)
            r_list.add_relation(r)
            all_file_pkg_node_list.append(entity_node)

    return r_list


# 生成工具包节点
# 寻找命令结点中类型为url的节点
def generate_tool_node(entity_list: List[EntityNode], edge_index_list: EdgeIndexList,
                       exe_cmd_node_list: List[ExecutableNode], config_entity_list: List[ConfigNode] = None,
                       file_path: str = "") -> RelationList:
    r_list: RelationList = RelationList()
    url_node_index_list: List = []
    all_exe_cmd_name = [exe_cmd.name for exe_cmd in exe_cmd_node_list]
    # 删除冗余边，只保留最近边
    new_edge_index_list = remove_redundant_edges_in_graph(edge_index_list)
    for idx, entity_node in enumerate(entity_list):
        if isinstance(entity_node, CommandNode) and entity_node.cmd_type == "url":
            url_node_index_list.append(idx)
    if url_node_index_list:
        for index in url_node_index_list:
            entity_node = entity_list[index]
            assert isinstance(entity_node, CommandNode)
            tool_pkg_node: ToolPkgNode = entity_node.to_tool_pkg_node(file_path)
            rel_set = find_tool_node(index, url_node_index_list, new_edge_index_list)
            # simplified_set = remove_redundant_edges(rel_set)
            all_step_entity_node: Set[StepNode] = set()

            # 生成安装块
            for id1, id2 in rel_set:
                entity1 = entity_list[id1]
                if isinstance(entity1, ImageNode):
                    continue
                entity2 = entity_list[id2]
                step_entity1 = StepNode(entity1, tool_pkg_node.url)
                step_entity2 = StepNode(entity2, tool_pkg_node.url)
                all_step_entity_node.add(step_entity1)
                all_step_entity_node.add(step_entity2)
                r: Relation = Relation(step_entity2, step_entity1, RType.Dependency)
                r_list.add_relation(r)

            # 生存安装块中所有用到的命令列表
            cmd_set = set()
            for step_entity in all_step_entity_node:
                entity = step_entity.entity_node
                if isinstance(entity, CommandNode) or isinstance(entity, PkgNode):
                    cmd = entity.name
                    if cmd in all_exe_cmd_name:
                        cmd_set.add(entity.name)
            # 填充工具包节点的命令列表
            tool_pkg_node.set_cmd_list(list(sorted(cmd_set)))
            # 填充工具包节点与安装块的依赖关系
            for entity in all_step_entity_node:
                r: Relation = Relation(tool_pkg_node, entity, RType.Has)
                r_list.add_relation(r)

            # 填充工具包节点与配置信息的依赖关系
            if config_entity_list:
                for config_entity in config_entity_list:
                    r: Relation = Relation(tool_pkg_node, config_entity, RType.Settings)
                    r_list.add_relation(r)

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


# 寻找所有包依赖，根据包依赖识别当前命令是否为系统原生命令
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


# 寻找指定节点的所有文件目录依赖
def find_all_file_dir_dependency(index: int, edge_index_list: EdgeIndexList) -> List[int]:
    pkg_index_list: List[int] = []
    for idx, d_type in enumerate(edge_index_list.type_list):
        if d_type == DDType.FILE_DIR:
            before_index = edge_index_list.edge_index_list[idx][0]
            file_pkg_idx = edge_index_list.edge_index_list[idx][1]
            if index == file_pkg_idx:
                pkg_index_list.append(before_index)

    return pkg_index_list


# 寻找工具包节点
def find_tool_node(start_node_index: int, all_url_index_list: List, edge_index_list: EdgeIndexList) -> Set[Tuple[int, int]]:
    before_dict, after_dict = gen_edge_index_dict(edge_index_list)
    rel_set = set()
    # 往前寻找
    queue = [start_node_index]
    while queue:
        cur_node_index = queue.pop(0)
        if cur_node_index in after_dict:
            for before_node_index in after_dict[cur_node_index]:
                if before_node_index in all_url_index_list:
                    continue
                if not is_env_dependency((before_node_index, cur_node_index), edge_index_list):
                    rel_set.add((before_node_index, cur_node_index))
                queue.append(before_node_index)

    # 向后寻找
    queue = [start_node_index]
    while queue:
        cur_node_index = queue.pop(0)
        if cur_node_index in before_dict:
            for after_node_index in before_dict[cur_node_index]:
                if after_node_index in all_url_index_list:
                    continue
                if not is_env_dependency((cur_node_index, after_node_index), edge_index_list):
                    rel_set.add((cur_node_index, after_node_index))
                queue.append(after_node_index)
    return rel_set


def gen_edge_index_dict(edge_index_list: EdgeIndexList) -> Tuple[Dict, Dict]:
    before_dict = dict()
    after_dict = dict()
    all_edge = edge_index_list.edge_index_list
    for edge in all_edge:
        before_dict[edge[0]] = before_dict.get(edge[0], []) + [edge[1]]
        after_dict[edge[1]] = after_dict.get(edge[1], []) + [edge[0]]
    return before_dict, after_dict


def remove_redundant_edges(dependencies):
    graph = {}
    for u, v in dependencies:
        if u not in graph:
            graph[u] = set()
        graph[u].add(v)

    edges_to_keep = set(dependencies)

    for u, v in dependencies:
        for w in graph.get(u, []):
            if v in graph.get(w, []):
                edges_to_keep.discard((u, v))

    result = list(edges_to_keep)
    return result


def is_env_dependency(edge: Tuple[int, int], edge_index_list: EdgeIndexList) -> bool:
    index = edge_index_list.edge_index_list.index(edge)
    if edge_index_list.type_list[index] == DDType.ENV_VAR:
        return True
    return False
