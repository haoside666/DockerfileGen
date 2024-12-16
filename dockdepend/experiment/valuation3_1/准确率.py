# !/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei', 'KaiTi', 'FangSong']  # 汉字字体,优先使用黑体，如果找不到黑体，则使用楷体
plt.rcParams['font.size'] = 8  # 字体大小
plt.rcParams['axes.unicode_minus'] = False

df = pd.read_excel("../data/去除基础镜像结果表.xlsx", index_col=0)
tool_percentage_list = [int(item * 100) for item in df["tool_correct_percentage"].to_list()]
print(sum(tool_percentage_list) / 100)
text_percentage_list = [int(item * 100) for item in df["text_correct_percentage"].to_list()]
print(sum(text_percentage_list) / 100)
wxyy_percentage_list = [int(item * 100) for item in df["wxyy_correct_percentage"].to_list()]
print(sum(wxyy_percentage_list) / 100)
enrie_percentage_list = [int(item * 100) for item in df["enrie_correct_percentage"].to_list()]
print(sum(enrie_percentage_list) / 100)
chatgpt_percentage_list = [int(item * 100) for item in df["chatgpt_correct_percentage"].to_list()]
print(sum(chatgpt_percentage_list) / 100)
N = 5

# 创建一个图形和N个子图
fig, axs = plt.subplots(nrows=N, ncols=1, figsize=(7, 5))

# 为每个数组绘制柱状图
axs[0].bar(np.arange(100), text_percentage_list, color="#696969")
axs[1].bar(np.arange(100), tool_percentage_list, color="#696969")
axs[2].bar(np.arange(100), wxyy_percentage_list, color="#696969")
axs[3].bar(np.arange(100), enrie_percentage_list, color="#696969")
axs[4].bar(np.arange(100), chatgpt_percentage_list, color="#696969")

# 设置每个子图的标题和标签
axs[0].set_title('(a) 关键词匹配')
axs[1].set_title('(b) DockDepend')
axs[2].set_title('(c) 文心一言模型')
axs[3].set_title('(d) ENRIE-4.0模型')
axs[4].set_title('(e) chatgpt4.0模型')
axs[0].set_xlabel('样本序号')
axs[1].set_xlabel('样本序号')
axs[2].set_xlabel('样本序号')
axs[3].set_xlabel('样本序号')
axs[4].set_xlabel('样本序号')
axs[0].set_ylabel('准确率(%)')
axs[1].set_ylabel('准确率(%)')
axs[2].set_ylabel('准确率(%)')
axs[3].set_ylabel('准确率(%)')
axs[4].set_ylabel('准确率(%)')

# axs[0].legend(labels=['text'], loc='upper right', fontsize=8)
# axs[1].legend(labels=['tool'], loc='upper right', fontsize=8)
# axs[2].legend(labels=['wxyy'], loc='upper right', fontsize=8)

# 调整子图之间的间距
plt.tight_layout()

# 显示图形
# plt.show()

plt.savefig("图7 准确率对比图.jpg", bbox_inches='tight')
