import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 创建DataFrame对象（即二维表格）
df = pd.DataFrame([
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 2, 0, 0, 0, 0, 0, 0, 0, 3, 20, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 4, 5, 5, 5, 6, 7, 7, 5, 5, 5, 0, 5, 0, 0, 0, 0, 0],
    [0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 22, 0, 0, 0, 0, 0, 0, 0],
    [0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 22, 0, 0, 0, 0, 0, 0, 0],
    [0, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 11, 0, 0, 0, 0, 0, 0, 0, 0, 21, 0, 0, 0, 0, 0, 0, 0],
    [0, 12, 0, 0, 0, 0, 13, 13, 0, 21, 0, 0, 0, 0, 0, 0, 0, 0],
    [15, 14, 15, 15, 15, 16, 17, 17, 15, 15, 15, 16, 15, 15, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 18, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 19, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
])

# 创建一个新的figure和axes对象
fig, ax = plt.subplots()

# 隐藏x轴和y轴的刻度和标签
ax.set_xticks([])
ax.set_yticks([])
ax.set_xticklabels([])
ax.set_yticklabels([])

columns = ['FROM',
           'RUN',
           'CMD',
           'LABEL',
           'MAINTAINER',
           'EXPOSE',
           'ENV',
           'ADD',
           'COPY',
           'ENTRYPOINT',
           'VOLUME',
           'USER',
           'WORKDIR',
           'ARG',
           'ONBUILD',
           'STOPSIGNAL',
           'HEALTHCHECK',
           'SHELL']
# 使用table函数创建表格
the_table = ax.table(cellText=df.values, colLabels=columns, rowLabels=columns, cellLoc='center', loc='center')

# 调整表格和单元格的边框
the_table.auto_set_font_size(False)
the_table.set_fontsize(14)
the_table.scale(1, 1.5)
for (row, col), cell in the_table.get_celld().items():
    cell.set_width(0.02)  # 设置列宽
    cell.set_height(0.02)  # 设置行高
    cell.set_edgecolor('black')

# 隐藏轴线
ax.axis('off')

# # 显示图表
# plt.show()

# 保存图表为图片
plt.savefig('table_image.png')
