import os.path
import sys

import dockerfile
from typing import List, Optional
from dockdepend.dockerfile_process.datatypes.DockerfileMeta import DockerfileMeta
from dockdepend.dockerfile_process.datatypes.DockerfilePrimitiveMeta import DockerfilePrimitiveMeta
from dockdepend.dockerfile_process.datatypes.InstructMetaList import InstructMetaList
from dockdepend.dockerfile_process.datatypes.PrimitiveMetaList import PrimitiveMetaList
from dockdepend.dockerfile_process.preprocess.datatypes.InstructMetaInit import InstructMetaInit
from dockdepend.dockerfile_process.preprocess.datatypes.InstructMetaPrefix import InstructMetaPrefix
from dockerfile import Command
from dockdepend.dockerfile_process.preprocess import Preprocess
from dockdepend.exception.CustomizedException import InstructFormatError, InstructNotFoundError, \
    ParsingException, SyntaxNonSupportError


def process(dockerfile_name: str, build_ctx: str) -> Optional[DockerfilePrimitiveMeta]:
    if not os.path.exists(dockerfile_name) or not os.path.isfile(dockerfile_name):
        print(f'error: {dockerfile_name} path does not exist or it is not a file!!!')
        return None
    if not os.path.exists(build_ctx) or not os.path.isdir(build_ctx):
        print(f'error: {build_ctx} path does not exist or it is not a directory!!!')
        return None
    with open(dockerfile_name, "r") as dfh:
        try:
            parsed_dockerfile: List[Command] = dockerfile.parse_string(dfh.read())
            dockerfile_meta: DockerfileMeta = DockerfileMeta(parsed_dockerfile)
            dockerfile_primitive_meta: DockerfilePrimitiveMeta = DockerfilePrimitiveMeta(dockerfile_meta.is_mutil_stage)
            for stage in dockerfile_meta.stage_list:
                cmd_meta_init_list: List[InstructMetaInit] = []
                for command in stage.cmd_list:
                    cmd_meta_init_list.append(Preprocess.preprocess(command, build_ctx))
                stage_meta_prefix_list: List[InstructMetaPrefix] = [InstructMetaPrefix(item.cmd_name, item.get_operand())
                                                                    for item in cmd_meta_init_list]
                dockerfile_meta.add_element_to_stage_meta_init_list(stage_meta_prefix_list)
                instruct_meta_list: InstructMetaList = InstructMetaList(build_ctx, cmd_meta_init_list)
                p_meta_list: PrimitiveMetaList = PrimitiveMetaList(build_ctx, instruct_meta_list)
                dockerfile_primitive_meta.add_element_to_stage_meta_list(p_meta_list)
            return dockerfile_primitive_meta
        except (InstructNotFoundError, InstructFormatError, SyntaxNonSupportError) as e:
            print(f"ERROR: {e}！", file=sys.stderr)
            return None
        except ParsingException:
            print(f"ERROR: {dockerfile_name} shell parse exception！", file=sys.stderr)
            return None
        except Exception as e:
            print(type(e).__name__, file=sys.stderr)
            print(f"ERROR: {dockerfile_name} exception!!！", file=sys.stderr)
            raise
