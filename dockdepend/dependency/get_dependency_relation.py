from dockdepend.dependency.datatypes.DDType import DDType
from dockdepend.dockerfile_process.datatypes.PrimitiveMetaList import PrimitiveMetaList
from dockdepend.dockerfile_process.preprocess.datatypes.PrimitiveMeta import PrimitiveMeta
from dockdepend.dependency.datatypes.EdgeIndexList import EdgeIndexList
from dockdepend.dependency.dependency_judge import dependency_judge, have_instruct_no_order_in_instruct_name_list
from typing import List


def get_dependency_relation(command_meta_list: PrimitiveMetaList) -> EdgeIndexList:
    edge_index_list: EdgeIndexList = EdgeIndexList()
    p_meta_list: List[PrimitiveMeta] = command_meta_list.p_meta_list
    length = len(p_meta_list)
    if length < 2:
        return edge_index_list
    for i in range(0, length - 1):
        cmd_name1 = p_meta_list[i].cmd_name
        if cmd_name1 == "WORKDIR" or cmd_name1 == "USER":
            j = i
            for j in range(i + 1, length):
                cmd_name2 = p_meta_list[j].cmd_name
                if cmd_name1 == cmd_name2:
                    break
            end = j + 1
        else:
            end = length
        for j in range(i + 1, end):
            dd_type, msg = dependency_judge(p_meta_list[i], p_meta_list[j])
            if dd_type.value:
                edge_index_list.add_element_to_edge_index_list((i, j), dd_type, msg)

    __get_workdir_or_user_addition_relation(command_meta_list, edge_index_list)
    __get_group_addition_relation(command_meta_list, edge_index_list)
    return edge_index_list


def __get_workdir_or_user_addition_relation(command_meta_list: PrimitiveMetaList, edge_index_list: EdgeIndexList):
    instruct_name_list = [item.cmd_name for item in command_meta_list.p_meta_list]
    if "USER" in instruct_name_list and have_instruct_no_order_in_instruct_name_list(instruct_name_list):
        index_list = __get_all_match_item_index("USER", instruct_name_list)
        __ensure_dependencies_on_the_last_workdir_or_user(index_list, edge_index_list)

    if "WORKDIR" in instruct_name_list and have_instruct_no_order_in_instruct_name_list(instruct_name_list):
        index_list = __get_all_match_item_index("WORKDIR", instruct_name_list)
        __ensure_dependencies_on_the_last_workdir_or_user(index_list, edge_index_list)


def __get_group_addition_relation(command_meta_list: PrimitiveMetaList, edge_index_list: EdgeIndexList):
    current_group_id = 0
    for idx, p_meta in enumerate(command_meta_list.p_meta_list):
        if p_meta.cmd_name == "RUN":
            if p_meta.is_master:
                current_group_id = idx
            else:
                edge_index_list.add_element_to_edge_index_list((current_group_id, idx), DDType.BASIC_GROUP, "Group dependency")


def __ensure_dependencies_on_the_last_workdir_or_user(index_list: List[int], edge_index_list: EdgeIndexList):
    if len(index_list) > 1:
        last_index = index_list[-1]
        length = len(index_list) - 1
        for i in range(length):
            start_index = index_list[i]
            end_index_list = edge_index_list.get_all_edge_end_index_by_start_index(start_index)
            if len(end_index_list) == 0:
                edge_index_list.add_element_to_edge_index_list((start_index, last_index), DDType.BOOT,
                                                               "Boot dependency")
            else:
                for index in end_index_list:
                    edge_index_list.add_element_to_edge_index_list((index, last_index), DDType.BOOT,
                                                                   "Boot dependency")
        # for i in range(length):
        #     for j in range(i + 1, length):
        #         edge_index_list.add_element_to_edge_index_list((index_list[i], index_list[j]))


def __get_all_match_item_index(match_item: str, match_list: List[str]) -> List[int]:
    index_list = []
    for index in range(len(match_list)):
        if match_list[index] == match_item:
            index_list.append(index)
    return index_list
