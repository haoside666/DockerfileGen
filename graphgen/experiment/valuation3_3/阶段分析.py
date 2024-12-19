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
            if line.startswith("\t("):
                line = line.split("#")[0].replace("\t", "")[:-1]
                r_list.append(line)
        project_list1.append(copy.deepcopy(name))
        dependency_list1.append(copy.deepcopy(r_list))

project_list2 = []
dependency_list2 = []
for filename in os.listdir("./stage1"):
    with open(f"./stage1/{filename}", "r", encoding="utf-8") as file:
        name = filename.split("###")[0]

        r_list = []
        for line in file:
            if line.startswith("\t("):
                line = line.split("#")[0].replace("\t", "")[:-1]
                r_list.append(line)
        project_list2.append(copy.deepcopy(name))
        dependency_list2.append(copy.deepcopy(r_list))

project_list3 = []
dependency_list3 = []
for filename in os.listdir("./stage2"):
    with open(f"./stage2/{filename}", "r", encoding="utf-8") as file:
        name = filename.split("###")[0]

        r_list = []
        for line in file:
            if line.startswith("\t("):
                line = line.split("#")[0].replace("\t", "")[:-1]
                r_list.append(line)
        project_list3.append(copy.deepcopy(name))
        dependency_list3.append(copy.deepcopy(r_list))

project_list4 = []
dependency_list4 = []
d = dict()
for filename in os.listdir("./stage3"):
    name = filename.split("###")[0]
    with open(f"./stage3/{filename}", "r", encoding="utf-8") as file:
        dependency_info = json.loads(file.read())
        for item in dependency_info:
            r_list.append(item["edge"])
    project_list4.append(copy.deepcopy(name))
    dependency_list4.append(copy.deepcopy(r_list))

if project_list1 == project_list2 and project_list1 == project_list3 and project_list1 == project_list4:
    d["project"] = project_list1
    d["artificial_result"] = dependency_list1
    d["stage1"] = dependency_list2
    d["stage2"] = dependency_list3
    d["stage3"] = dependency_list4

df = pd.DataFrame(data=d)

new_df = df[["project"]].copy()
new_df["stage1"] = df["stage1"].apply(lambda x: [item for item in x if not item.startswith("(0")]).copy()
new_df["stage2"] = df["stage2"].apply(lambda x: [item for item in x if not item.startswith("(0")]).copy()
new_df["stage3"] = df["stage3"].apply(lambda x: [item for item in x if not item.startswith("(0")]).copy()
new_df["artificial_result"] = df["artificial_result"].apply(
    lambda x: [item for item in x if not item.startswith("(0")]).copy()


def count_same(row, column1, column2):
    return len(set(row[column1]) & set(row[column2]))


def get_size_and_correct_amount(df):
    df["artificial_result_size"] = df["artificial_result"].apply(np.size)
    df["stage1_size"] = df["stage1"].apply(np.size)
    df["stage2_size"] = df["stage2"].apply(np.size)
    df["stage3_size"] = df["stage3"].apply(np.size)

    df["stage1_same"] = df.apply(
        lambda row: count_same(row, "stage1", "artificial_result"), axis=1)
    df["stage2_same"] = df.apply(
        lambda row: count_same(row, "stage2", "artificial_result"), axis=1)
    df["stage3_same"] = df.apply(
        lambda row: count_same(row, "stage3", "artificial_result"), axis=1)

    # df["tool_no_correct_amount"] = df["tool_result_size"] - df["tool_correct_amount"]
    # df["text_no_correct_amount"] = df["text_result_size"] - df["text_correct_amount"]


def get_percentage(df):
    df["diff_stage1"] = df["stage1_same"] / df["artificial_result_size"]
    df["diff_stage2"] = (df["stage2_same"] - df["stage1_same"]) / df["artificial_result_size"]
    df["diff_stage3"] = (df["stage3_same"] - df["stage2_same"]) / df["artificial_result_size"]
    # df["tool_no_correct_percentage"] = df["tool_no_correct_amount"] / df["artificial_result_size"]
    # df["text_no_correct_percentage"] = df["text_no_correct_amount"] / df["artificial_result_size"]


# def fill_nan_or_inf(df):
#     df = df.fillna(1/3)
#     df = df.replace([np.inf, -np.inf])
#     return df


def get_info(df):
    get_size_and_correct_amount(df)
    get_percentage(df)
    # df = fill_nan_or_inf(df)
    return df


new_df = get_info(new_df)
new_df.to_excel("./去除基础镜像阶段分析表.xlsx")
df = get_info(df)
df.to_excel("./阶段分析表.xlsx")
