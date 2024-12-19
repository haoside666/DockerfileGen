import argparse
from graphgen.arg_module.ast_module import add_ast_module
from graphgen.arg_module.dependency_module import add_dependency_module
from graphgen.arg_module.extractor_module import add_extractor_module
from graphgen.arg_module.meta_module import add_meta_module


def main():
    # 程序名
    prog = "graphgen"
    # 创建主解析器
    tool_description = '%(prog)s 是一个Dockerfile依赖关系解析器,用于解析Dockerfile并得到其中所有指令行之间的依赖关系。'
    parser = argparse.ArgumentParser(prog=prog, usage='%(prog)s [-h] <子模块> [<参数>]',
                                     description=tool_description,
                                     epilog='使用dockdepend <子模块> -h 获取给定子模块的帮助文档。\n\n')

    subparsers = parser.add_subparsers(title="子模块", description="可选的子模块", required=True,
                                       help='子模块功能介绍', metavar='  子模块名   ')

    # 添加 dependency 模块
    add_dependency_module(prog, subparsers)
    # 添加 meta 模块
    add_meta_module(prog, subparsers)
    # 添加 ast 模块
    add_ast_module(prog, subparsers)
    # 添加 extractor 模块
    add_extractor_module(prog, subparsers)

    # 解析参数
    args = parser.parse_args()

    # 调用了与当前选定的子命令相关联的函数
    args.func(args)
    return 0


# Functionality is not yet complete
#
if __name__ == '__main__':
    main()
