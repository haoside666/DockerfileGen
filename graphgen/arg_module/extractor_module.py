import json
import os
import sys

from graphgen.dockerfile_process.datatypes.InstructFeature import InstructFeature
from graphgen.exception.CustomizedException import ParameterMissError, ParsingException
from graphgen.extractor.extractor_cli import get_command_list_feature, get_command_list_parse_result
from graphgen.shell_parse.parse import parse_shell_script_file_to_instruct_feature, \
    parse_file_all_command_to_instruct_feature


def add_extractor_module(prog, subparsers):
    extractor_module_description = '输入一个shell脚本文件或脚本目录，得到经过ast分析和特征提取后的指令特征结构'
    extractor_parser = subparsers.add_parser('extractor', prog=prog,
                                             usage='%(prog)s extractor (-f <file_path>| -d <dir_path>) [<选项>]',
                                             description=extractor_module_description,
                                             help='extractor模块,得到shell命令经过ast分析和特征提取后的结果')
    extractor_group = extractor_parser.add_mutually_exclusive_group()
    extractor_group.add_argument('-f', '--file', type=str, help='输入单个shell脚本的文件路径')
    extractor_group.add_argument('-d', '--dir', type=str, help='输入含有多个shell脚本的目录路径')
    extractor_parser.add_argument('-o', '--output', default=sys.stdout, type=str, required=False,
                                  help='输出路径,默认标准输出')
    extractor_parser.add_argument('--current_user', default='root', type=str, required=False,
                                  help='指定当前用户，默认用户为root')
    extractor_parser.add_argument('--current_dir', default='/tmp', type=str, required=False,
                                  help='指定输入脚本文件或脚本目录的位置,默认目录/tmp')
    extractor_parser.add_argument('--only-parse', action='store_true', default=False,
                                  help='只进行命令解析，注意该操作会丢弃经过ast分析后的命令特征结构中除了命令列表外的所有字段信息')
    extractor_parser.add_argument('--detach', action='store_true', default=False, help='分离命令，以最小命令为基元')
    extractor_parser.set_defaults(func=extractor_module_func)


def script_file_feature_parse(file_path, output_path, current_user, current_dir):
    try:
        if output_path != sys.stdout and not os.path.isfile(output_path) and "." not in output_path:
            print(f'ERROR: {output_path} is not a file!!! please enter a file path', file=sys.stderr)
            return
        init_instruct_feature = parse_shell_script_file_to_instruct_feature(file_path)
        if init_instruct_feature:
            cmd_list_feat, attribute_dir = get_command_list_feature(init_instruct_feature.command_list, current_user,
                                                                    current_dir)
            instruct_feat: InstructFeature = InstructFeature(init_instruct_feature, cmd_list_feat, current_user)
            # 去除未知命令集合
            instruct_feat.pkg_set = {x for x in instruct_feat.pkg_set if not x.startswith("unknown_")}
            if output_path == sys.stdout:
                print(json.dumps(instruct_feat.to_dict(), indent=4))
            else:
                with open(output_path, 'w') as file:
                    file.write(json.dumps(instruct_feat.to_dict(), indent=4))
        else:
            print(f'ERROR: {file_path} does not contain valid shell commands!', file=sys.stderr)
            return
    except ParsingException as e:
        print(f'ParsingException: shell script parse error!', file=sys.stderr)
        return


def script_file_all_command_feature_parse(file_path, output_path, current_user, current_dir):
    try:
        if output_path != sys.stdout and not os.path.isfile(output_path) and "." not in output_path:
            print(f'ERROR: {output_path} is not a file!!! please enter a file path', file=sys.stderr)
            return
        instruct_feature_init_list = parse_file_all_command_to_instruct_feature(file_path)
        if instruct_feature_init_list:
            lis = []
            for command, init_instruct_feature in instruct_feature_init_list:
                cmd_list_feat, attribute_dir = get_command_list_feature(init_instruct_feature.command_list,
                                                                        current_user,
                                                                        current_dir)
                instruct_feat: InstructFeature = InstructFeature(init_instruct_feature, cmd_list_feat, current_user)
                # 去除未知命令集合
                instruct_feat.pkg_set = {x for x in instruct_feat.pkg_set if not x.startswith("unknown_")}
                if output_path == sys.stdout:
                    feat_dict = dict()
                    feat_dict["command"] = command
                    feat_dict["result"] = instruct_feat.to_dict()
                    print(json.dumps(feat_dict, indent=4) + '\n')
                else:
                    feat_dict = dict()
                    feat_dict["command"] = command
                    feat_dict["result"] = instruct_feat.to_dict()
                    lis.append(feat_dict)
            if output_path != sys.stdout:
                with open(output_path, 'w') as file:
                    file.write(json.dumps(lis, indent=4))
        else:
            print(f'ERROR: {file_path} does not contain valid shell commands!', file=sys.stderr)
            return
    except ParsingException as e:
        print(f'ParsingException: shell script parse error!', file=sys.stderr)
        return


def script_file_only_parse(file_path, output_path):
    try:
        if output_path != sys.stdout and not os.path.isfile(output_path) and "." not in output_path:
            print(f'ERROR: {output_path} is not a file!!! please enter a file path', file=sys.stderr)
            return
        init_instruct_feature = parse_shell_script_file_to_instruct_feature(file_path)
        if init_instruct_feature:
            parse_result = get_command_list_parse_result(init_instruct_feature.command_list)

            output = ""
            for command, result in parse_result:
                if isinstance(command, str):
                    cmd_parse_dict = dict()
                    cmd_parse_dict["command"] = command
                    cmd_parse_dict["parse_result"] = result.to_dict()
                    output += "======================================================================\n"
                    output += json.dumps(cmd_parse_dict, indent=4) + "\n"

                elif isinstance(command, list):
                    cmd_parse_dict = dict()
                    cmd_parse_dict["command"] = command
                    for idx, item in enumerate(result):
                        cmd_parse_dict[f"parse {idx + 1}"] = item.to_dict()
                    output += "======================================================================\n"
                    output += json.dumps(cmd_parse_dict, indent=4) + "\n"

            if output_path == sys.stdout:
                print(output)
            else:
                with open(output_path, 'w') as file:
                    file.write(output)
        else:
            print(f'ERROR: {file_path} does not contain valid shell commands!', file=sys.stderr)
            return
    except ParsingException as e:
        print(f'ParsingException: shell script parse error!', file=sys.stderr)
        return


def extractor_module_func(args):
    file_path = args.file
    dir_path = args.dir
    output_path = args.output
    current_user = args.current_user
    current_dir = args.current_dir
    only_parse = args.only_parse
    is_detach = args.detach
    if file_path is None and dir_path is None:
        raise ParameterMissError("args error: please enter a file path or directory path")
    if file_path and dir_path:
        print("ERROR: -f and -d option can not be used at the same time!", file=sys.stderr)
        return

    if file_path:
        if only_parse:
            script_file_only_parse(file_path, output_path)
        else:
            if is_detach:
                script_file_all_command_feature_parse(file_path, output_path, current_user, current_dir)
            else:
                script_file_feature_parse(file_path, output_path, current_user, current_dir)
    elif dir_path:
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
                if output_path == sys.stdout:
                    print(f'-------------------------{file_path}----------------------------')
                    if only_parse:
                        script_file_only_parse(file_path, output_path)
                    elif is_detach:
                        script_file_all_command_feature_parse(file_path, output_path, current_user, current_dir)
                    else:
                        script_file_feature_parse(file_path, output_path, current_user, current_dir)
                else:
                    if only_parse:
                        new_output_path = os.path.join(output_path, os.path.splitext(file_name)[0] + "_Parse.txt")
                        script_file_only_parse(file_path, new_output_path)
                    elif is_detach:
                        new_output_path = os.path.join(output_path,
                                                       os.path.splitext(file_name)[0] + "_Feature_DETACH.json")
                        script_file_all_command_feature_parse(file_path, new_output_path, current_user, current_dir)
                    else:
                        new_output_path = os.path.join(output_path, os.path.splitext(file_name)[0] + "_Feature.json")
                        script_file_feature_parse(file_path, new_output_path, current_user, current_dir)
