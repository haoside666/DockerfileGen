from dockdepend.dependency.datatypes.DDType import DDType
from dockdepend.dockerfile_process.datatypes.InstructMetaList import InstructMetaList
from dockdepend.dockerfile_process.preprocess.datatypes.InstructMeta import InstructMeta
from dockdepend.dependency.datatypes.EdgeIndexList import EdgeIndexList
from dockdepend.dependency.dependency_judge import dependency_judge, have_instruct_no_order_in_instruct_name_list
from typing import List


def get_dependency_relation(command_meta_list: InstructMetaList) -> EdgeIndexList:
    edge_index_list: EdgeIndexList = EdgeIndexList()
    cmd_meta_list: List[InstructMeta] = command_meta_list.cmd_meta_list
    length = len(cmd_meta_list)
    if length < 2:
        return edge_index_list
    for i in range(0, length - 1):
        cmd_name1 = cmd_meta_list[i].cmd_name
        if cmd_name1 == "WORKDIR" or cmd_name1 == "USER":
            j = i
            for j in range(i + 1, length):
                cmd_name2 = cmd_meta_list[j].cmd_name
                if cmd_name1 == cmd_name2:
                    break
            end = j + 1
        else:
            end = length
        for j in range(i + 1, end):
            dd_type, msg = dependency_judge(cmd_meta_list[i], cmd_meta_list[j])
            if dd_type.value:
                edge_index_list.add_element_to_edge_index_list((i, j), dd_type, msg)

    __get_workdir_or_user_addition_relation(command_meta_list, edge_index_list)
    return edge_index_list


def __get_workdir_or_user_addition_relation(command_meta_list: InstructMetaList, edge_index_list: EdgeIndexList):
    instruct_name_list = [item.cmd_name for item in command_meta_list.cmd_meta_list]
    if "USER" in instruct_name_list and have_instruct_no_order_in_instruct_name_list(instruct_name_list):
        index_list = __get_all_match_item_index("USER", instruct_name_list)
        __ensure_dependencies_on_the_last_workdir_or_user(index_list, edge_index_list)

    if "WORKDIR" in instruct_name_list and have_instruct_no_order_in_instruct_name_list(instruct_name_list):
        index_list = __get_all_match_item_index("WORKDIR", instruct_name_list)
        __ensure_dependencies_on_the_last_workdir_or_user(index_list, edge_index_list)


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
