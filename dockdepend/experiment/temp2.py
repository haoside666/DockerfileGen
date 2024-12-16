import os.path
import shutil

import matplotlib

print(matplotlib.matplotlib_fname())

import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['SimHei', 'KaiTi', 'FangSong']  # 汉字字体,优先使用黑体，如果找不到黑体，则使用楷体
plt.rcParams['font.size'] = 12  # 字体大小
plt.rcParams['axes.unicode_minus'] = False

x = np.linspace(-8, 8, 1024)
y1 = 0.618 * np.abs(x) - 0.8 * np.sqrt(64 - x ** 2)
y2 = 0.618 * np.abs(x) + 0.8 * np.sqrt(64 - x ** 2)
plt.plot(x, y1, color='r')
plt.plot(x, y2, color='r')
plt.title("我爱C语言中文网", fontsize=20, color="b")
plt.show()

# with open("./filename", "r") as file:
#     filename_list = [line.strip() for line in file]
#
# for item in filename_list:
#     root_path = "./dockerfile/original"
#     dir_name = item.replace("/", "___")
#     filename = os.listdir(os.path.join(root_path, dir_name))[0]
#     src_file = os.path.join(dir_name, filename)
#     dst_file = os.path.join("./output",filename)
#     shutil.copy(src_file, dst_file)
