import json
import os
import sys
from dockdepend.exception.CustomizedException import ParameterMissError, ParsingException
from dockdepend.shell_parse.parse import parse_shell_script_file_to_instruct_feature, get_raw_asts, \
    parse_file_all_command_to_instruct_feature


def add_ast_module(prog, subparsers):
    ast_module_description = '输入一个shell脚本文件或脚本目录，得到经过AST分析后的初始指令特征结构'
    ast_parser = subparsers.add_parser('ast', prog=prog,
                                       usage='%(prog)s ast (-f <file_path>| -d <dir_path>) [<选项>]',
                                       description=ast_module_description,
                                       help='AST模块,得到shell命令经过AST分析后的结果')
    ast_group = ast_parser.add_mutually_exclusive_group()
    ast_group.add_argument('-f', '--file', type=str, help='输入单个shell脚本的文件路径')
    ast_group.add_argument('-d', '--dir', type=str, help='输入含有多个shell脚本的目录路径')
    ast_parser.add_argument('-o', '--output', default=sys.stdout, type=str, required=False,
                            help='输出路径,默认标准输出')
    ast_parser.add_argument('--raw', action='store_true', default=False, help='得到原始信息')
    ast_parser.add_argument('--detach', action='store_true', default=False, help='分离命令，以最小命令为基元')
    ast_parser.set_defaults(func=ast_module_func)


def script_file_ast_parse(file_path, output_path):
    try:
        if output_path != sys.stdout and not os.path.isfile(output_path) and "." not in output_path:
            print(f'ERROR: {output_path} is not a file!!! please enter a file path', file=sys.stderr)
            return
        init_instruct_feature = parse_shell_script_file_to_instruct_feature(file_path)
    except ParsingException as e:
        print(f'ParsingException: shell script parse error!', file=sys.stderr)
        return
    if init_instruct_feature is None:
        print(f'ERROR: {file_path} does not contain valid shell commands!', file=sys.stderr)
    else:
        if output_path == sys.stdout:
            print(json.dumps(init_instruct_feature.to_dict(), indent=4))
        else:
            with open(output_path, 'w') as file:
                file.write(json.dumps(init_instruct_feature.to_dict(), indent=4))


def script_file_all_command_ast_parse(file_path, output_path):
    try:
        if output_path != sys.stdout and not os.path.isfile(output_path) and "." not in output_path:
            print(f'ERROR: {output_path} is not a file!!! please enter a file path', file=sys.stderr)
            return
        instruct_feature_init_list = parse_file_all_command_to_instruct_feature(file_path)
    except ParsingException as e:
        print(f'ParsingException: shell script parse error!', file=sys.stderr)
        return
    if not instruct_feature_init_list:
        print(f'ERROR: {file_path} does not contain valid shell commands!', file=sys.stderr)
    else:
        if output_path == sys.stdout:
            for command, init_instruct_feature in instruct_feature_init_list:
                feat_dict = dict()
                feat_dict["command"] = command
                feat_dict["result"] = init_instruct_feature.to_dict()
                print(json.dumps(feat_dict, indent=4) + '\n')
        else:
            lis = []
            for command, init_instruct_feature in instruct_feature_init_list:
                feat_dict = dict()
                feat_dict["command"] = command
                feat_dict["result"] = init_instruct_feature.to_dict()
                lis.append(feat_dict)
            with open(output_path, 'w') as file:
                file.write(json.dumps(lis, indent=4))


def script_file_raw_parse(file_path, output_path):
    try:
        if output_path != sys.stdout and not os.path.isfile(output_path) and "." not in output_path:
            print(f'ERROR: {output_path} is not a file!!! please enter a file path', file=sys.stderr)
            return
        untyped_ast_objects = get_raw_asts(file_path)
    except ParsingException as e:
        print(f'ParsingException: shell script parse error!', file=sys.stderr)
        return
    if not untyped_ast_objects:
        print(f'ERROR: {file_path} does not contain valid shell commands!', file=sys.stderr)
    else:
        if output_path == sys.stdout:
            for ast_object in untyped_ast_objects:
                print(ast_object)
        else:
            with open(output_path, 'w') as file:
                output = []
                for ast_object in untyped_ast_objects:
                    output.append(str(ast_object))
                file.write('\n'.join(output))


def ast_module_func(args):
    file_path = args.file
    dir_path = args.dir
    output_path = args.output
    is_raw = args.raw
    is_detach = args.detach
    if file_path is None and dir_path is None:
        raise ParameterMissError("args error: please enter a file path or directory path")
    if file_path and dir_path:
        print("ERROR: -f and -d option can not be used at the same time!", file=sys.stderr)
        return
    if file_path:
        if is_raw:
            script_file_raw_parse(file_path, output_path)
        else:
            if is_detach:
                script_file_all_command_ast_parse(file_path, output_path)
            else:
                script_file_ast_parse(file_path, output_path)
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
                    if is_raw:
                        script_file_raw_parse(file_path, output_path)
                    elif is_detach:
                        script_file_ast_parse(file_path, output_path)
                    else:
                        script_file_all_command_ast_parse(file_path, output_path)
                else:
                    if is_raw:
                        new_output_path = os.path.join(output_path, os.path.splitext(file_name)[0] + "_raw.txt")
                        script_file_raw_parse(file_path, new_output_path)
                    elif is_detach:
                        new_output_path = os.path.join(output_path, os.path.splitext(file_name)[0] + "_AST_DETACH.json")
                        script_file_all_command_ast_parse(file_path, new_output_path)
                    else:
                        new_output_path = os.path.join(output_path, os.path.splitext(file_name)[0] + "_AST.json")
                        script_file_ast_parse(file_path, new_output_path)
