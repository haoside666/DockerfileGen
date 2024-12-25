import json
import logging
import os
import sys
import traceback
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import Optional, List

import dockerfile
from dockerfile import Command

from graphgen.config.definitions import ROOT_DIR
from graphgen.dockerfile_process.datatypes.DockerfilePrimitiveMeta import DockerfilePrimitiveMeta
from graphgen.dockerfile_process.datatypes.PrimitiveMetaList import PrimitiveMetaList
from graphgen.dockerfile_process.processer import processer, processer_mutil_process
from graphgen.exception.CustomizedException import ParameterMissError
from graphgen.graph.get_graph_info import gen_neo4j_script_by_meta

LOG_PATH = f"{ROOT_DIR}/../logs/errors.txt"
# 创建日志
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(filename=LOG_PATH, encoding='utf-8')
formatter = logging.Formatter('[{levelname}:{asctime}:{module}:{funcName}:{lineno}] {message}', style='{')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def add_graph_module(prog, subparsers):
    meta_module_description = '输入一个Dockerfile文件或Dockerfile文件目录,解析得到其中所有实体与关系的neo4j创建脚本'
    meta_parser = subparsers.add_parser('graph', prog=prog,
                                        usage='%(prog)s graph (-f <file_path>| -d <dir_path>) [<选项>]',
                                        description=meta_module_description,
                                        help='图谱创建模块,解析Dockerfile得到其中所有实体与关系的neo4j创建脚本')
    meta_group = meta_parser.add_mutually_exclusive_group()
    meta_group.add_argument('-f', '--file', type=str, help='输入单个Dockerfile的文件路径')
    meta_group.add_argument('-d', '--dir', type=str, help='输入含有多个Dockerfile的目录路径')
    meta_parser.add_argument('-o', '--output', default=sys.stdout, type=str, required=False,
                             help='输出路径,默认标准输出')
    meta_parser.set_defaults(func=meta_module_func)


# Printing command meta information in a pretty way for a dockerfile
def beautiful_neo4j_print(neo4j_script_str: str, out_path, current_num=1, stage_num=1):
    if stage_num == 1:
        if out_path == sys.stdout:
            print('// ===============================================================')
            print(neo4j_script_str)
        else:
            if not out_path.endswith(".cypher"):
                out_path = f'{out_path}_script.cypher'
            with open(out_path, "w") as file:
                file.write(neo4j_script_str)
    else:
        if out_path == sys.stdout:
            print('// =========================================================================')
            print(f'// -------------------------stage {current_num}----------------------------')
            print(neo4j_script_str)
        else:
            base_name, ext = os.path.splitext(out_path)
            out_path = f'{base_name}_{current_num}{ext}'
            with open(out_path, "w") as file:
                file.write(neo4j_script_str)


def dockerfile_graph_gen(arg):
    file_path, output_path, build_ctx = arg
    if output_path != sys.stdout and not os.path.isfile(output_path) and "." not in output_path:
        print(f'ERROR: {output_path} is not a file!!! please enter a file path', file=sys.stderr)
        logger.error(f'ERROR: {output_path} is not a file!!! please enter a file path')
        return file_path
    try:
        postfix = str(os.getpid())
        dockerfile_meta: Optional[DockerfilePrimitiveMeta] = processer(file_path, build_ctx, postfix)
        if dockerfile_meta is not None:
            stage_num = len(dockerfile_meta.stage_meta_list)
            if stage_num == 0:
                print("ERROR: Didn't parse to any valid build stage, make sure to include the FROM directive!",
                      file=sys.stderr)
                logger.error("ERROR: Didn't parse to any valid build stage, make sure to include the FROM directive!")
                return file_path

            for i in range(stage_num):
                stage_meta_list: PrimitiveMetaList = dockerfile_meta.stage_meta_list[i]
                neo4j_script = gen_neo4j_script_by_meta(stage_meta_list, file_path)
                beautiful_neo4j_print(neo4j_script, output_path, i + 1, stage_num)
        else:
            print(f'ERROR: {file_path} fails to be handled or the Dockerfile is incorrect!', file=sys.stderr)
            logger.error(f'ERROR: {file_path} fails to be handled or the Dockerfile is incorrect!')
        return file_path
    except dockerfile.GoParseError as e:
        print(f"ERROR: {e.args[0]}!", file=sys.stderr)
        logger.error(f"ERROR: {e.args[0]}!")
        return file_path
    except Exception as e:
        print(traceback.format_exc())
        logger.error("---------------------------------")
        logger.error(traceback.format_exc())
        logger.error("---------------------------------")
        print(f'ERROR: {file_path} fails to be handled or the Dockerfile is incorrect!', file=sys.stderr)
        print(f"ERROR: {e.args[0]}!", file=sys.stderr)
        return file_path


def dockerfile_graph_gen_with_mutil_process(arg):
    file_path, output_path, build_ctx, parsed_dockerfile = arg
    if output_path != sys.stdout and not os.path.isfile(output_path) and "." not in output_path:
        print(f'ERROR: {output_path} is not a file!!! please enter a file path', file=sys.stderr)
        logger.error(f'ERROR: {output_path} is not a file!!! please enter a file path')
        return file_path
    try:
        postfix = str(os.getpid())
        dockerfile_meta: Optional[DockerfilePrimitiveMeta] = processer_mutil_process(file_path, build_ctx, parsed_dockerfile, postfix)
        if dockerfile_meta is not None:
            stage_num = len(dockerfile_meta.stage_meta_list)
            if stage_num == 0:
                print("ERROR: Didn't parse to any valid build stage, make sure to include the FROM directive!",
                      file=sys.stderr)
                logger.error("ERROR: Didn't parse to any valid build stage, make sure to include the FROM directive!")
                return file_path

            for i in range(stage_num):
                stage_meta_list: PrimitiveMetaList = dockerfile_meta.stage_meta_list[i]
                neo4j_script = gen_neo4j_script_by_meta(stage_meta_list)
                beautiful_neo4j_print(neo4j_script, output_path, i + 1, stage_num)
        else:
            print(f'ERROR: {file_path} fails to be handled or the Dockerfile is incorrect!', file=sys.stderr)
            logger.error(f'ERROR: {file_path} fails to be handled or the Dockerfile is incorrect!')
        return file_path
    except dockerfile.GoParseError as e:
        print(f"ERROR: {e.args[0]}!", file=sys.stderr)
        logger.error(f"ERROR: {e.args[0]}!")
        return file_path
    except Exception as e:
        print(traceback.format_exc())
        logger.error("---------------------------------")
        logger.error(traceback.format_exc())
        logger.error("---------------------------------")
        print(f'ERROR: {file_path} fails to be handled or the Dockerfile is incorrect!', file=sys.stderr)
        print(f"ERROR: {e.args[0]}!", file=sys.stderr)
        return file_path


def clear_temp_file():
    dir_path = f"{ROOT_DIR}/shell_parse"
    for file_name in os.listdir(dir_path):
        if file_name.startswith("temp_cmd"):
            os.remove(os.path.join(dir_path, file_name))


def meta_module_func(args):
    file_path = args.file
    dir_path = args.dir
    output_path = args.output
    if file_path is None and dir_path is None:
        raise ParameterMissError("args error: please enter a file path or directory path")
    if file_path and dir_path:
        print("ERROR: -f and -d option can not be used at the same time!", file=sys.stderr)
        return
    clear_temp_file()
    if file_path:
        build_ctx = os.path.dirname(file_path)
        if build_ctx == '':
            build_ctx = '.'
        dockerfile_graph_gen((file_path, output_path, build_ctx))
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

        # for file_name in os.listdir(dir_path):
        #     file_path = os.path.join(dir_path, file_name)
        #     if os.path.isfile(file_path):
        #         print(f"----start handle {file_path}-----")
        #         if output_path != sys.stdout:
        #             new_output_path = os.path.join(output_path, os.path.splitext(file_name)[0] + "_script.cypher")
        #         else:
        #             print(f'-------------------------{file_path}----------------------------')
        #             new_output_path = output_path
        #         dockerfile_graph_gen(file_path, new_output_path, build_ctx)
        #         print(f"----handle {file_path} finish!!!")

        # 利用进程池进行并发处理
        if output_path != sys.stdout:
            arg_list = []
            for file_name in os.listdir(dir_path):
                file_path = os.path.join(dir_path, file_name)
                if not os.path.exists(file_path) or not os.path.isfile(file_path):
                    print(f'error: {file_path} path does not exist or it is not a file!!!')
                    continue
                if not os.path.exists(build_ctx) or not os.path.isdir(build_ctx):
                    print(f'error: {build_ctx} path does not exist or it is not a directory!!!')
                    continue
                try:
                    with open(file_path, "r") as dfh:
                        # dockerfile.parse_string 不支持多进程操作，放外部
                        parsed_dockerfile: List[Command] = dockerfile.parse_string(dfh.read())
                        new_output_path = os.path.join(output_path, os.path.splitext(file_name)[0] + "_script.cypher")
                        arg_list.append((file_path, new_output_path, build_ctx, parsed_dockerfile))
                except:
                    print(f'ERROR: {file_path} 调用parse_string解析失败!', file=sys.stderr, flush=True)
                    # 删除无效文件
                    # os.remove(file_path)
                    continue
            with ProcessPoolExecutor(max_workers=4) as executor:
                futures = {executor.submit(dockerfile_graph_gen_with_mutil_process, arg): arg for arg in arg_list}
                for future in as_completed(futures):
                    try:
                        result = future.result()
                        # Process the result
                        print(result)
                    except TimeoutError:
                        print("Task timed out")
                    except Exception as e:
                        print(f"Task generated an exception: {e}")
        else:
            for file_name in os.listdir(dir_path):
                file_path = os.path.join(dir_path, file_name)
                if os.path.isfile(file_path):
                    print(f'-------------------------{file_path}----------------------------')
                    new_output_path = output_path
                    dockerfile_graph_gen((file_path, new_output_path, build_ctx))
