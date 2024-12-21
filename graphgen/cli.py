import argparse
import os

from graphgen.arg_module.dependency_module import add_dependency_module
from graphgen.arg_module.meta_module import add_meta_module
from graphgen.arg_module.graph_module import add_graph_module


def main():
    try:
        # 程序名
        prog = "dockerfileGen"
        # 创建主解析器
        tool_description = '%(prog)s 是一个Dockerfile自动生成工具。'
        parser = argparse.ArgumentParser(prog=prog, usage='%(prog)s [-h] <子模块> [<参数>]',
                                         description=tool_description,
                                         epilog='dockerfileGen <子模块> -h 获取给定子模块的帮助文档。\n\n')

        subparsers = parser.add_subparsers(title="子模块", description="可选的子模块", required=True,
                                           help='子模块功能介绍', metavar='  子模块名   ')

        # 添加 dependency 模块
        add_dependency_module(prog, subparsers)
        # 添加 meta 模块
        add_meta_module(prog, subparsers)
        # 添加 graph 模块
        add_graph_module(prog, subparsers)

        # 解析参数
        args = parser.parse_args()

        # 调用了与当前选定的子命令相关联的函数
        args.func(args)
    except FileNotFoundError as e:
        dir_path = os.path.dirname(e.filename)
        os.makedirs(dir_path, exist_ok=True)
        print(f"{dir_path}不存在，现在已经创建!")
    except Exception as e:
        raise
    return 0


# Functionality is not yet complete
#
if __name__ == '__main__':
    main()
