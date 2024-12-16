import json
import os
import sys
from typing import Optional

import dockerfile

from dockdepend.dockerfile_process.datatypes.DockerfileMeta import DockerfileMeta
from dockdepend.dockerfile_process.process import process
from dockdepend.exception.CustomizedException import ParameterMissError


def add_meta_module(prog, subparsers):
    meta_module_description = '输入一个Dockerfile文件或Dockerfile文件目录,得到经过数据处理后的meta结构'
    meta_parser = subparsers.add_parser('meta', prog=prog,
                                        usage='%(prog)s meta (-f <file_path>| -d <dir_path>) [<选项>]',
                                        description=meta_module_description,
                                        help='元信息模块,得到经过数据预处理器处理后的元信息')
    meta_group = meta_parser.add_mutually_exclusive_group()
    meta_group.add_argument('-f', '--file', type=str, help='输入单个Dockerfile的文件路径')
    meta_group.add_argument('-d', '--dir', type=str, help='输入含有多个Dockerfile的目录路径')
    meta_parser.add_argument('-o', '--output', default=sys.stdout, type=str, required=False,
                             help='输出路径,默认标准输出')
    meta_parser.set_defaults(func=meta_module_func)


# Printing command meta information in a pretty way for a dockerfile
def beautiful_command_meta_print(command_meta_list, out_path, current_num=1, stage_num=1):
    lis = []
    cmd_meta_list = command_meta_list.cmd_meta_list
    for command_mete in cmd_meta_list:
        d = dict()
        d["Original"] = command_mete.pretty()
        d["Meta"] = command_mete.to_dict()
        lis.append(d)
    if stage_num == 1:
        if out_path == sys.stdout:
            print('===============================================================')
            print(json.dumps(lis, indent=4))
        else:
            with open(out_path, "w") as file:
                file.write(json.dumps(lis, indent=4))
    else:
        if out_path == sys.stdout:
            print('=========================================================================')
            print(f'-------------------------stage {current_num}----------------------------')
            print(json.dumps(lis, indent=4))
        else:
            base_name, ext = os.path.splitext(out_path)
            out_path = f'{base_name}_{current_num}{ext}'
            with open(out_path, "w") as file:
                file.write(json.dumps(lis, indent=4))


def dockerfile_meta_parse(file_path, output_path, build_ctx):
    if output_path != sys.stdout and not os.path.isfile(output_path) and "." not in output_path:
        print(f'ERROR: {output_path} is not a file!!! please enter a file path', file=sys.stderr)
        return
    try:
        dockerfile_meta: Optional[DockerfileMeta] = process(file_path, build_ctx)
    except dockerfile.GoParseError as e:
        print(f"ERROR: {e.args[0]}!", file=sys.stderr)
        return
    except Exception as e:
        print(f"ERROR: {e.args[0]}!", file=sys.stderr)
        return

    if dockerfile_meta is not None:
        stage_num = len(dockerfile_meta.stage_meta_list)
        if stage_num == 0:
            print("ERROR: Didn't parse to any valid build stage, make sure to include the FROM directive!",
                  file=sys.stderr)
            return

        for i in range(stage_num):
            command_meta_list = dockerfile_meta.stage_meta_list[i]
            beautiful_command_meta_print(command_meta_list, output_path, i + 1, stage_num)
    else:
        print(f'ERROR: {file_path} fails to be handled or the Dockerfile is incorrect!', file=sys.stderr)


def meta_module_func(args):
    file_path = args.file
    dir_path = args.dir
    output_path = args.output
    if file_path is None and dir_path is None:
        raise ParameterMissError("args error: please enter a file path or directory path")
    if file_path and dir_path:
        print("ERROR: -f and -d option can not be used at the same time!", file=sys.stderr)
        return

    if file_path:
        build_ctx = os.path.dirname(file_path)
        if build_ctx == '':
            build_ctx = '.'
        dockerfile_meta_parse(file_path, output_path, build_ctx)
    elif dir_path:
        build_ctx = dir_path
        if not os.path.isdir(dir_path):
            print(f'ERROR: {dir_path} is not a directory!!! please enter a directory path!', file=sys.stderr)
            return
        if output_path != sys.stdout:
            if '.' in os.path.basename(output_path):
                print('ERROR: When using the -d option, the -o option must be a directory path!',
                      file=sys.stderr)
                return
            os.makedirs(output_path, exist_ok=True)

        for file_name in os.listdir(dir_path):
            file_path = os.path.join(dir_path, file_name)
            if os.path.isfile(file_path):
                if output_path != sys.stdout:
                    new_output_path = os.path.join(output_path, os.path.splitext(file_name)[0] + "_meta.json")
                else:
                    print(f'-------------------------{file_path}----------------------------')
                    new_output_path = output_path
                dockerfile_meta_parse(file_path, new_output_path, build_ctx)
