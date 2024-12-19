import json
import os
import sys
import time
from typing import Optional, List

import dockerfile

from graphgen.dependency.datatypes.DDType import DDType
from graphgen.dependency.datatypes.EdgeIndexList import EdgeIndexList
from graphgen.dependency.get_dependency_relation import get_dependency_relation
from graphgen.dockerfile_process.datatypes.DockerfileMeta import DockerfileMeta
from graphgen.dockerfile_process.preprocess.datatypes.InstructMeta import InstructMeta
from graphgen.dockerfile_process.process import process
from graphgen.config import global_config

from graphgen.exception.CustomizedException import ParameterMissError


def add_dependency_module(prog, subparsers):
    dependency_module_description = '输入一个Dockerfile文件或Dockerfile文件目录,得到文件每个阶段指令行间的依赖关系'
    usage = '%(prog)s dependency [-f <file_path>| -d <dir_path>] [(--simple-mode | --no-instruct-mode)] [<选项>]'
    dependency_parser = subparsers.add_parser('dependency', prog=prog,
                                              usage=usage,
                                              description=dependency_module_description,
                                              help='依赖模块,得到指令行间的依赖关系')
    dependency_group = dependency_parser.add_mutually_exclusive_group()
    dependency_group.add_argument('-f', '--file', type=str, help='输入单个Dockerfile的文件路径')
    dependency_group.add_argument('-d', '--dir', type=str, help='输入含有多个Dockerfile的目录路径')
    dependency_parser.add_argument('-o', '--output', default=sys.stdout, type=str, required=False,
                                   help='输出路径,默认标准输出')
    dependency_parser.add_argument('--build-info', action='store_true', default=False,
                                   help='获取构建时间，依赖数量，指令数等信息,显示所有依赖，不支持--ignore-side-effect等选项')
    dependency_group2 = dependency_parser.add_mutually_exclusive_group()
    dependency_group2.add_argument('--simple-mode', action='store_true', default=False,
                                   help='简单模式，只输出依赖指令行号对')
    dependency_group2.add_argument('--no-instruct-mode', action='store_true', default=False,
                                   help='不输出指令模式，不输出原指令信息对')
    dependency_parser.add_argument('--ignore-side-effect', action='store_true', default=False,
                                   help='不显示副作用影响依赖')
    dependency_parser.add_argument('--ignore-unknown-command', action='store_true', default=False,
                                   help='不显示未识别命令依赖')
    dependency_parser.add_argument('--show-consistency-dependency', action='store_true', default=False,
                                   help='显示一致性依赖')
    dependency_parser.set_defaults(func=dependency_module_func)


# def get_filter_msg_list(ignore_side_effect, ignore_unknown_command, show_consistency_dependency):
#     filter_list = []
#     if ignore_side_effect:
#         filter_list.append(DDType.SIDE_EFFECT)
#     if ignore_unknown_command:
#         filter_list.append(DDType.UNKNOWN_COMMAND)
#     if not show_consistency_dependency:
#         filter_list.append(DDType.CONSISTENCY)
#     return filter_list


def get_mode(simple_mode, no_instruct_mode):
    if simple_mode:
        return 'simple'
    elif no_instruct_mode:
        return 'no_instruct'
    else:
        return 'default'


def get_default_mode_result(edge_index_list: EdgeIndexList, meta_list: List[InstructMeta]):
    lis = []
    for idx, edge in enumerate(edge_index_list.edge_index_list):
        d = dict()
        before, after = edge
        d['before_instruct'] = meta_list[before].pretty()
        d['after_instruct'] = meta_list[after].pretty()
        d['edge'] = str(edge)
        d['type'] = edge_index_list.type_list[idx].name
        d['dependency_description'] = edge_index_list.msg_list[idx]
        lis.append(d)
    return lis


def get_simple_mode_result(edge_index_list: EdgeIndexList):
    return edge_index_list.edge_index_list


def get_no_instruct_mode_result(edge_index_list: EdgeIndexList):
    lis = []
    for idx, edge in enumerate(edge_index_list.edge_index_list):
        d = dict()
        d['edge'] = str(edge)
        d['type'] = edge_index_list.type_list[idx].name
        d['dependency_description'] = edge_index_list.msg_list[idx]
        lis.append(d)
    return lis


def beautiful_command_dependency_print(command_meta_list, edge_index_list, out_path, current_num=1, stage_num=1,
                                       mode='default'):
    if stage_num == 1:
        if out_path == sys.stdout:
            print('===============================================================')
            if mode == 'default':
                print(json.dumps(get_default_mode_result(edge_index_list, command_meta_list.cmd_meta_list), indent=4))
            elif mode == 'simple':
                print(get_simple_mode_result(edge_index_list))
            elif mode == 'no_instruct':
                print(json.dumps(get_no_instruct_mode_result(edge_index_list), indent=4))
        else:
            with open(out_path, "w") as file:
                if mode == 'default':
                    file.write(
                        json.dumps(get_default_mode_result(edge_index_list, command_meta_list.cmd_meta_list), indent=4))
                elif mode == 'simple':
                    file.write(str(get_simple_mode_result(edge_index_list)))
                elif mode == 'no_instruct':
                    file.write(json.dumps(get_no_instruct_mode_result(edge_index_list), indent=4))
    else:
        if out_path == sys.stdout:
            print('=========================================================================')
            print(f'-------------------------stage {current_num}----------------------------')
            if mode == 'default':
                print(json.dumps(get_default_mode_result(edge_index_list, command_meta_list.cmd_meta_list), indent=4))
            elif mode == 'simple':
                print(get_simple_mode_result(edge_index_list))
            elif mode == 'no_instruct':
                print(json.dumps(get_no_instruct_mode_result(edge_index_list), indent=4))
        else:
            base_name, ext = os.path.splitext(out_path)
            out_path = f'{base_name}_{current_num}{ext}'
            with open(out_path, "w") as file:
                if mode == 'default':
                    file.write(
                        json.dumps(get_default_mode_result(edge_index_list, command_meta_list.cmd_meta_list), indent=4))
                elif mode == 'simple':
                    file.write(str(get_simple_mode_result(edge_index_list)))
                elif mode == 'no_instruct':
                    file.write(json.dumps(get_no_instruct_mode_result(edge_index_list), indent=4))


def beautiful_build_info_print(build_info, out_path, current_num=1, stage_num=1):
    if stage_num == 1:
        if out_path == sys.stdout:
            print('===============================================================')
            print(json.dumps(build_info, indent=4))
        else:
            with open(out_path, "w") as file:
                file.write(json.dumps(build_info, indent=4))
    else:
        if out_path == sys.stdout:
            print('=========================================================================')
            print(f'-------------------------stage {current_num}----------------------------')
            print(json.dumps(build_info, indent=4))
        else:
            base_name, ext = os.path.splitext(out_path)
            out_path = f'{base_name}_{current_num}{ext}'
            with open(out_path, "w") as file:
                file.write(json.dumps(build_info, indent=4))


def dockerfile_dependency_parse(file_path, output_path, build_ctx, mode):
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
            edge_index_list: EdgeIndexList = get_dependency_relation(command_meta_list)
            beautiful_command_dependency_print(command_meta_list, edge_index_list, output_path, i + 1, stage_num, mode)
    else:
        print(f'ERROR: {file_path} fails to be handled or the Dockerfile is incorrect!', file=sys.stderr)


def dockerfile_build_info(file_path, output_path, build_ctx):
    if output_path != sys.stdout and not os.path.isfile(output_path) and "." not in output_path:
        print(f'ERROR: {output_path} is not a file!!! please enter a file path', file=sys.stderr)
        return
    build_info = dict()
    start_time = time.time()
    filename = os.path.basename(file_path)
    build_info["filename"] = filename
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
            build_info["command_length"] = command_meta_list.length()
            edge_index_list: EdgeIndexList = get_dependency_relation(command_meta_list)
            end_time = time.time()
            build_info["processing_time"] = end_time - start_time
            build_info["dependency_count"] = edge_index_list.length()
            build_info["dependency"] = str(edge_index_list.edge_index_list)
            build_info['dependency_description'] = str(edge_index_list.msg_list)
            beautiful_build_info_print(build_info, output_path, i + 1, stage_num)
    else:
        print(f'ERROR: {file_path} fails to be handled or the Dockerfile is incorrect!', file=sys.stderr)


def dependency_module_func(args):
    file_path = args.file
    dir_path = args.dir
    output_path = args.output
    build_info = args.build_info
    simple_mode = args.simple_mode
    no_instruct_mode = args.no_instruct_mode
    global_config.ignore_side_effect = args.ignore_side_effect
    global_config.ignore_unknown_command = args.ignore_unknown_command
    global_config.show_consistency_dependency = args.show_consistency_dependency

    if file_path is None and dir_path is None:
        raise ParameterMissError("args error: please enter a file path or directory path")
    if file_path and dir_path:
        print("ERROR: -f and -d option can not be used at the same time!", file=sys.stderr)
        return

    mode = get_mode(simple_mode, no_instruct_mode)

    if file_path:
        build_ctx = os.path.dirname(file_path)
        if build_ctx == '':
            build_ctx = '.'
        if build_info:
            dockerfile_build_info(file_path, output_path, build_ctx)
        else:
            dockerfile_dependency_parse(file_path, output_path, build_ctx, mode)
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
                    new_output_path = os.path.join(output_path, os.path.splitext(file_name)[0] + "_dependency.json")
                else:
                    print(f'-------------------------{file_path}----------------------------')
                    new_output_path = output_path

                if build_info:
                    dockerfile_build_info(file_path, os.path.join(output_path, file_name + "_build-info"), build_ctx)
                else:
                    dockerfile_dependency_parse(file_path, new_output_path, build_ctx, mode)
