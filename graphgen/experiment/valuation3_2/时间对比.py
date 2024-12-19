import json

import pandas as pd
import os
import copy
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei', 'KaiTi', 'FangSong']  # 汉字字体,优先使用黑体，如果找不到黑体，则使用楷体
plt.rcParams['font.size'] = 12  # 字体大小
plt.rcParams['axes.unicode_minus'] = False
# project_list = []
# time_list = []
# for filename in os.listdir("./人工标注_result"):
#     with open(f"./人工标注_result/{filename}", "r", encoding="utf-8") as file:
#         name = filename.split("###")[0]
#         time = 0
#         for line in file:
#             if line.startswith("所用时间："):
#                 time = line.replace("所用时间：", "").strip()
#                 break
#         project_list.append(name)
#         time_list.append(time)
#
# data = {
#     "project": project_list,
#     "use_time": time_list,
# }
# df = pd.DataFrame(data=data)
pd.set_option('display.max_columns', None)


def get_tool_build_info():
    project_list = []
    tool_processing_time_list = []
    for filename in os.listdir("../tool_build-info"):
        with open(f"../tool_build-info/{filename}", "r", encoding="utf-8") as file:
            content = file.read()
            d = json.loads(content)
            project_name = d["filename"].split("###")[0].lower()
            tool_processing_time = d["processing_time"]
            project_list.append(project_name)
            tool_processing_time_list.append(tool_processing_time)

    data = dict()
    data["project"] = project_list
    data["tool_processing_time"] = tool_processing_time_list
    df = pd.DataFrame(data=data)
    return df


def calc_file_char_num(content):
    dockerfile_content = []
    for line in content.split('\n')[1:-1]:
        if line.strip():
            dockerfile_content.append(line)

    char_num = len("\n".join(dockerfile_content))
    return char_num


def get_model_build_info():
    project_list = []
    model_processing_time_list = []
    char_length_list = []
    instruction_length_list = []
    for filename in os.listdir("../ENRIE-4-8k_result"):
        if filename.endswith("-cost_time") and not filename.startswith("test.txt"):
            original_filename = filename.replace("-cost_time", "")
            with open("../提问模板/" + original_filename, "r", encoding="utf-8") as file:
                content = file.read()
                char_num = calc_file_char_num(content)
                project_name = filename.split("###")[0].lower()

            with open("../ENRIE-4-8k_result/" + filename, "r", encoding="utf-8") as file:
                lines = file.readlines()
                assert len(lines) == 2
                instruction_length = float(lines[0].strip())
                cost_time = float(lines[1].strip())

            project_list.append(project_name)
            model_processing_time_list.append(cost_time)
            char_length_list.append(char_num)
            instruction_length_list.append(instruction_length)

    data = dict()
    data["project"] = project_list
    data["model_processing_time"] = model_processing_time_list
    data["char_length"] = char_length_list
    data["instruction_length"] = instruction_length_list
    df = pd.DataFrame(data=data)
    return df


tool_df = get_tool_build_info()
artificial_df = pd.read_excel("../data/人工标注时间表.xlsx", index_col=0)
artificial_df = artificial_df[["project", "use_time"]]
artificial_df["project"] = artificial_df["project"].apply(lambda x: x.lower())
model_df = get_model_build_info()


union_df = pd.merge(artificial_df, tool_df, on="project")
union_df = pd.merge(union_df, model_df, on="project")
print(union_df.describe())

fig = plt.figure()
# 添加绘图区域
ax = fig.add_axes((0.1, 0.1, 0.8, 0.8))
ax.scatter(union_df["instruction_length"].tolist(), union_df["use_time"].tolist(), color='#808080',
           label="人工用时")
ax.scatter(union_df["instruction_length"].tolist(), union_df["model_processing_time"].tolist(), color='#000000',
           label="ERNIE-4.0用时")
ax.scatter(union_df["instruction_length"].tolist(), union_df["tool_processing_time"].tolist(), color='#DCDCDC',
           label="DockDepend用时")
# ax.set_yscale('log')
ax.set_xlabel('指令行数量/行')
ax.set_ylabel('用时(s)')
# ax.set_title('人工与DockDepend用时散点图')
# 添加图例
plt.legend()
# plt.show()
plt.savefig("./图8 三种方式用时散点图.png")
