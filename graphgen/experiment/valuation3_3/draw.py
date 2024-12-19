import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

plt.rcParams['font.sans-serif'] = ['SimHei', 'KaiTi', 'FangSong']  # 汉字字体,优先使用黑体，如果找不到黑体，则使用楷体
plt.rcParams['font.size'] = 12  # 字体大小
plt.rcParams['axes.unicode_minus'] = False
df = pd.read_excel("./去除基础镜像阶段分析表.xlsx", index_col=0)
df = df.fillna(1 / 3)
stage1 = df["diff_stage1"].to_numpy()*100
stage2 = df["diff_stage2"].to_numpy()*100
stage3 = df["diff_stage3"].to_numpy()*100
stage3_buttom = (df["diff_stage1"] + df["diff_stage2"]).to_numpy()*100

ind = df.index.tolist()

plt.figure(figsize=(12, 3))
# 获取当前轴对象
# ax = plt.gca()

# 设置x轴刻度的最大数量
# ax.xaxis.set_major_locator(MaxNLocator(30))
# ax.yaxis.set_major_locator(MaxNLocator(10))
# 绘制堆叠图
plt.bar(ind, stage3, width=0.8, label='stage3', color='#000000', bottom=stage3_buttom)
plt.bar(ind, stage2, width=0.8, label='stage2', color='#A9A9A9', bottom=stage1)
plt.bar(ind, stage1, width=0.8, label='stage1', color='#DCDCDC')
# 设置坐标轴
plt.ylabel("构建率(%)")
plt.xlabel("样本序号", labelpad=-6)
# plt.xlim([0,100])
plt.legend(loc="upper right")
# plt.show()
plt.savefig("图9 各阶段堆叠图.jpg", dpi=300, bbox_inches='tight')
