import os.path
from typing import Dict, List

from jinja2 import Environment, FileSystemLoader

current_dir = os.path.dirname(__file__)


def generate_graph_html(dockerfile: str, node_labels: Dict, edge_list: List[List]):
    # 配置模板环境
    env = Environment(loader=FileSystemLoader(current_dir))

    # 获取模板
    template = env.get_template('graph_echarts_template.html')

    # 渲染模板
    rendered_template = template.render(nodeLabels=node_labels, edgeList=edge_list)

    # 输出渲染后的模板
    # print(rendered_template)

    # 强制写入
    force = False
    file_path = os.path.join(current_dir, f'./{dockerfile}.html')
    if not force and os.path.exists(file_path):
        print("写入失败,文件已存在!")
    else:
        if force:
            print("注意:已强制覆盖!")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(rendered_template)
        print(f"生成{dockerfile}.html成功!!!")
