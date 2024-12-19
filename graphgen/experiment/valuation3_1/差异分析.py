import copy
import json
import os
from enum import Enum

import pandas as pd


def get_tool_dependency_result_info():
    project_list = []
    edges_list = []
    instructs_list = []
    dependency_types_list = []
    dependency_reasons_list = []
    for filename in os.listdir("../tool_result"):
        name = filename.split("###")[0]
        with open(f"../tool_result/{filename}", "r", encoding="utf-8") as file:
            edge_list = []
            instruct_list = []
            dependency_type_list = []
            dependency_reason_list = []
            dependency_info = json.loads(file.read())
            for item in dependency_info:
                edge_list.append(item["edge"])
                before_instruct_name = item["before_instruct"].split()[0]
                after_instruct_name = item["after_instruct"].split()[0]
                instruct_list.append((before_instruct_name, after_instruct_name))
                dependency_type_list.append(item["type"])
                dependency_reason_list.append(item["dependency_description"])

        project_list.append(copy.deepcopy(name))
        edges_list.append(copy.deepcopy(edge_list))
        instructs_list.append(copy.deepcopy(instruct_list))
        dependency_types_list.append(copy.deepcopy(dependency_type_list))
        dependency_reasons_list.append(copy.deepcopy(dependency_reason_list))

    return project_list, edges_list, instructs_list, dependency_types_list, dependency_reasons_list


df = pd.read_excel("../data/去除基础镜像结果表.xlsx", index_col=0)

diff_dict = dict()
diff_instruct_list = []
diff_dependency_type_list = []
diff_dependency_reason_list = []
project_list, edges_list, instructs_list, dependency_types_list, dependency_reasons_list = get_tool_dependency_result_info()
for row in df.itertuples():
    tool_result = json.loads(row.tool_result.replace("'", '"'))
    text_result = json.loads(row.text_result.replace("'", '"'))
    wxyy_result = json.loads(row.wxyy_result.replace("'", '"'))
    enrie_result = json.loads(row.enrie_result.replace("'", '"'))
    chatgpt_result = json.loads(row.chatgpt_result.replace("'", '"'))
    artificial_result = json.loads(row.artificial_result.replace("'", '"'))

    # 文本匹配和文心一言结果并集
    union_result = set(text_result) | set(wxyy_result) | set(enrie_result) | set(chatgpt_result)
    # 人工匹配结果和工具交集
    common_result = set(tool_result) & set(artificial_result)

    diff_result = common_result - union_result
    if diff_result:
        project_name = row.project
        print("------------------------------------------------")
        print(f"当前工程名为: {project_name}")
        print(f"工具比文本和大语言模型多出的结果：{diff_result}")
        idx = project_list.index(project_name)
        for edge in diff_result:
            redundant_element_index = edges_list[idx].index(edge)
            instruct = instructs_list[idx][redundant_element_index]
            dependency_type = dependency_types_list[idx][redundant_element_index]
            dependency_reason = dependency_reasons_list[idx][redundant_element_index]
            print(f"当前前后指令为：{instruct}")
            print(f"多余的依赖关系为：{dependency_type}, 原因是{dependency_reason}")
            diff_instruct_list.append(instruct)
            diff_dependency_type_list.append(dependency_type)
            diff_dependency_reason_list.append(dependency_reason)

diff_dict["instruct"] = diff_instruct_list
diff_dict["dependency_type"] = diff_dependency_type_list
diff_dict["dependency_reason"] = diff_dependency_reason_list

diff_df = pd.DataFrame(diff_dict)

# 相同依赖类型和指令进行聚合统计
same_dependency_type_and_instruct_df = diff_df.groupby(["dependency_type", "instruct"]).size().reset_index(
    name="count")
# 按聚合统计结果进行排序
same_dependency_type_and_instruct_df.sort_values(by="count", ascending=False, inplace=True)
# print(same_dependency_type_and_instruct_df)
# NONE = 0  # 无依赖
# BASIC_IMAGE = 1  # Image dependency
# BASIC_USER = 2  # User dependency
# BASIC_ONBUILD = 3  # OnBuild dependency
# RUN_PKG = 4  # have shell pkg intersection
# RUN_IO = 5  # have shell io intersection
# RUN_VAR = 6  # have shell var intersection
# RUN_OTHER = 7  # have shell other intersection
# RUN_USER1 = 9  # shell command user is different from the USER instruction
# RUN_USER2 = 10  # the shell command contains the user in the USER instruction
# ENV_VAR = 11  # environment variable dependencies
# ENV_VAR_IMPLICIT = 12  # system level environment variable dependencies(implicit)
# FILE_DIR = 13  # exist file or directory dependency
# SHELL_RUN = 14  # SHELL instruction dependency
# BOOT = 15  # Boot dependency
# SIDE_EFFECT = 8  # instruction contain side effect command
# UNKNOWN_COMMAND = 16  # instruction has unrecognized command
# CONSISTENCY = 17  # consistency dependency
DDType_tranform_dict = {
    "NONE": 0,
    "BASIC_IMAGE": 1,
    "BASIC_USER": 2,
    "BASIC_ONBUILD": 3,
    "RUN_PKG": 4,
    "RUN_IO": 5,
    "RUN_VAR": 6,
    "RUN_OTHER": 7,
    "RUN_USER1": 9,
    "RUN_USER2": 10,
    "ENV_VAR": 11,
    "ENV_VAR_IMPLICIT": 12,
    "FILE_DIR": 13,
    "SHELL_RUN": 14,
    "BOOT": 15,
    "SIDE_EFFECT": 8,
    "UNKNOWN_COMMAND": 16
}

# 利用枚举类型进行类型转变
same_dependency_type_and_instruct_df["dependency_type"] = same_dependency_type_and_instruct_df.apply(
    lambda row: DDType_tranform_dict[row["dependency_type"]], axis=1)
print(same_dependency_type_and_instruct_df[:10])
