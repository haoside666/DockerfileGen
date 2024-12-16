import copy
import json
import os

import numpy as np
import pandas as pd

project_list1 = []
dependency_list1 = []
d = dict()
for filename in os.listdir("./人工标注_result"):
    with open(f"./人工标注_result/{filename}", "r", encoding="utf-8") as file:
        name = filename.split("###")[0]

        r_list = []
        for line in file:
            if line.strip().startswith("("):
                line = line.split("#")[0].replace("\t", "")[:-1].strip()
                r_list.append(line)
        project_list1.append(copy.deepcopy(name))
        dependency_list1.append(copy.deepcopy(r_list))

project_list2 = []
dependency_list2 = []
for filename in os.listdir("./tool_result"):
    name = filename.split("###")[0]
    r_list = []
    with open(f"./tool_result/{filename}", "r", encoding="utf-8") as file:
        dependency_info = json.loads(file.read())
        for item in dependency_info:
            r_list.append(item["edge"])
    project_list2.append(copy.deepcopy(name))
    dependency_list2.append(copy.deepcopy(r_list))

project_list3 = []
dependency_list3 = []
for filename in os.listdir("./文本匹配_result"):
    with open(f"./文本匹配_result/{filename}", "r", encoding="utf-8") as file:
        name = filename.split("###")[0]

        r_list = []
        for line in file:
            if line.strip().startswith("("):
                line = line.split("#")[0].replace("\t", "")[:-1].strip()
                r_list.append(line)
        project_list3.append(copy.deepcopy(name))
        dependency_list3.append(copy.deepcopy(r_list))

project_list4 = []
dependency_list4 = []
d = dict()
for filename in os.listdir("./文心一言_result_new"):
    with open(f"./文心一言_result_new/{filename}", "r", encoding="utf-8") as file:
        name = filename.split("###")[0]

        r_list = []
        for line in file:
            if line.startswith("[(") or line.strip().startswith('('):
                t = line.split("(")[1].split(")")[0].strip()
                line = f'({t})'
                r_list.append(line)
        project_list4.append(copy.deepcopy(name))
        dependency_list4.append(copy.deepcopy(r_list))

project_list5 = []
dependency_list5 = []
d = dict()
for filename in os.listdir("./ENRIE-4-8k_result"):
    if filename.endswith(".txt") and filename != "test.txt":
        with open(f"./ENRIE-4-8k_result/{filename}", "r", encoding="utf-8") as file:
            name = filename.split("###")[0]

            r_list = []
            for line in file:
                if line.startswith("[(") or line.strip().startswith('('):
                    t = line.split("(")[1].split(")")[0].strip()
                    line = f'({t})'
                    r_list.append(line)
            project_list5.append(copy.deepcopy(name))
            dependency_list5.append(copy.deepcopy(r_list))

project_list6 = []
dependency_list6 = []
d = dict()
for filename in os.listdir("./chatgpt_result"):
    if filename.endswith(".txt") and filename != "test.txt":
        with open(f"./chatgpt_result/{filename}", "r", encoding="utf-8") as file:
            name = filename.split("###")[0]

            r_list = []
            for line in file:
                if line.startswith("[(") or line.strip().startswith('('):
                    t = line.split("(")[1].split(")")[0].strip()
                    line = f'({t})'
                    r_list.append(line)
            project_list6.append(copy.deepcopy(name))
            dependency_list6.append(copy.deepcopy(r_list))

if (project_list1 == project_list2 and project_list1 == project_list3 and project_list1 == project_list4
        and project_list1 == project_list5 and project_list1 == project_list6):
    d["project"] = project_list1
    d["artificial_result"] = dependency_list1
    d["tool_result"] = dependency_list2
    d["text_result"] = dependency_list3
    d["wxyy_result"] = dependency_list4
    d["enrie_result"] = dependency_list5
    d["chatgpt_result"] = dependency_list6

df = pd.DataFrame(data=d)

new_df = df[["project"]].copy()
new_df["tool_result"] = df["tool_result"].apply(lambda x: [item for item in x if not item.startswith("(0")]).copy()
new_df["text_result"] = df["text_result"].apply(lambda x: [item for item in x if not item.startswith("(0")]).copy()
new_df["wxyy_result"] = df["wxyy_result"].apply(lambda x: [item for item in x if not item.startswith("(0")]).copy()
new_df["enrie_result"] = df["enrie_result"].apply(lambda x: [item for item in x if not item.startswith("(0")]).copy()
new_df["chatgpt_result"] = df["chatgpt_result"].apply(
    lambda x: [item for item in x if not item.startswith("(0")]).copy()
new_df["artificial_result"] = df["artificial_result"].apply(
    lambda x: [item for item in x if not item.startswith("(0")]).copy()


def count_same(row, column1, column2):
    return len(set(row[column1]) & set(row[column2]))


def get_size_and_correct_amount(df):
    df["tool_result_size"] = df["tool_result"].apply(np.size)
    df["artificial_result_size"] = df["artificial_result"].apply(np.size)
    df["text_result_size"] = df["text_result"].apply(np.size)
    df["wxyy_result_size"] = df["wxyy_result"].apply(np.size)
    df["enrie_result_size"] = df["enrie_result"].apply(np.size)
    df["chatgpt_result_size"] = df["chatgpt_result"].apply(np.size)

    df["tool_correct_amount"] = df.apply(
        lambda row: count_same(row, "tool_result", "artificial_result"), axis=1)
    df["text_correct_amount"] = df.apply(
        lambda row: count_same(row, "text_result", "artificial_result"), axis=1)
    df["wxyy_correct_amount"] = df.apply(
        lambda row: count_same(row, "wxyy_result", "artificial_result"), axis=1)

    df["enrie_correct_amount"] = df.apply(
        lambda row: count_same(row, "enrie_result", "artificial_result"), axis=1)

    df["chatgpt_correct_amount"] = df.apply(
        lambda row: count_same(row, "chatgpt_result", "artificial_result"), axis=1)

    # df["tool_no_correct_amount"] = df["tool_result_size"] - df["tool_correct_amount"]
    # df["text_no_correct_amount"] = df["text_result_size"] - df["text_correct_amount"]


def get_percentage(df):
    df["tool_correct_percentage"] = df["tool_correct_amount"] / df["artificial_result_size"]
    df["text_correct_percentage"] = df["text_correct_amount"] / df["artificial_result_size"]
    df["wxyy_correct_percentage"] = df["wxyy_correct_amount"] / df["artificial_result_size"]
    df["enrie_correct_percentage"] = df["enrie_correct_amount"] / df["artificial_result_size"]
    df["chatgpt_correct_percentage"] = df["chatgpt_correct_amount"] / df["artificial_result_size"]
    # df["tool_no_correct_percentage"] = df["tool_no_correct_amount"] / df["artificial_result_size"]
    # df["text_no_correct_percentage"] = df["text_no_correct_amount"] / df["artificial_result_size"]


def fill_nan_or_inf(df):
    df = df.fillna(1)
    df = df.replace([np.inf, -np.inf])
    return df


def get_info(df):
    get_size_and_correct_amount(df)
    get_percentage(df)
    df = fill_nan_or_inf(df)
    return df


def generate_new_df_by_read_excel():
    new_df = pd.read_excel("./data/去除基础镜像结果表.xlsx", index_col=0)
    new_df = new_df[["project", "tool_result", "text_result", "wxyy_result", "enrie_result", "chatgpt_result",
                     "artificial_result"]].copy()
    new_df["tool_result"] = new_df["tool_result"].apply(lambda x: eval(x))
    new_df["text_result"] = new_df["text_result"].apply(lambda x: eval(x))
    new_df["wxyy_result"] = new_df["wxyy_result"].apply(lambda x: eval(x))
    new_df["enrie_result"] = new_df["enrie_result"].apply(lambda x: eval(x))
    new_df["chatgpt_result"] = new_df["chatgpt_result"].apply(lambda x: eval(x))
    new_df["artificial_result"] = new_df["artificial_result"].apply(lambda x: eval(x))
    return new_df


# def merge_and_label(row):
#     merged_values = []
#     merged_values.append((row['same1_percentage'], 1))
#     merged_values.append((row['same2_percentage'], 2))
#
#     # 将合并后的值和标签转换为所需的格式（这里假设是元组列表）
#     return merged_values
#
#
# df_new = df_filled[["same1_percentage", "same2_percentage"]]
# # 应用函数到每一行，并创建一个新列来存储结果
# df_new['merged'] = df_new.apply(merge_and_label, axis=1)
# df_new = df_new.explode("merged")
#
#
# def split_func(line):
#     line["percentage"] = line["merged"][0]
#     line["type"] = line["merged"][1]
#     return line
#
#
# df_new = df_new.apply(split_func, axis=1)
# import matplotlib.pyplot as plt
# import seaborn as sns
#
# sns.set(style="whitegrid")  # 设置样式为白色网格
# sns.set(rc={'figure.figsize': (11.7, 8.27)})  # 设置画布大小为长11.7,宽8.27
# ax = sns.boxplot(x="type", y="percentage", data=df_new)
# plt.show()

# import pyecharts.options as opts
# from pyecharts.charts import Line
# c = (
#     Line()
#     .add_xaxis(df_filled.index.to_list()) # list
#     .add_yaxis("same1", df_filled["no_same1_percentage"].to_list()) # list
#     .add_yaxis("same2", df_filled["no_same2_percentage"].to_list()) # list
#     .set_global_opts(title_opts=opts.TitleOpts(title="整体PV折线图"))
# )
# c.render()


new_df = generate_new_df_by_read_excel()
new_df = get_info(new_df)
new_df.to_excel("./data/去除基础镜像结果表.xlsx")
df = get_info(df)
df.to_excel("./data/原始结果表.xlsx")

# length = len(dependency_list1)
#
# total_same_num = 0
# total_artificial_num = 0
# for i in range(length):
#     artificial_dependency = set(dependency_list1[i])
#     tool_dependency = set(dependency_list2[i])
#     artificial_num = len(artificial_dependency)
#     tool_num = len(tool_dependency)
#     same_num = len(artificial_dependency & tool_dependency)
#     print(f'{i}----- {same_num} {tool_num} {same_num} {same_num / artificial_num}')
#     total_same_num += same_num
#     total_artificial_num += artificial_num
#
# print(total_same_num/total_artificial_num)
