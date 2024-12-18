from dockdepend.dockerfile_process.preprocess.datatypes.InstructMeta import InstructMeta
from dockdepend.dependency.datatypes.DType import DType
from .datatypes.DDType import DDType
from .judgeor.JudgeAddRun import JudgeAddRun
from .judgeor.JudgeArgDict import JudgeArgDict
from .judgeor.JudgeArgDir import JudgeArgDir
from .judgeor.JudgeArgRun import JudgeArgRun
from .judgeor.JudgeArgTuple import JudgeArgTuple
from .judgeor.JudgeCopyRun import JudgeCopyRun
from .judgeor.JudgeEnvDict import JudgeEnvDict
from .judgeor.JudgeEnvDir import JudgeEnvDir
from .judgeor.JudgeEnvRun import JudgeEnvRun
from .judgeor.JudgeEnvTuple import JudgeEnvTuple
from .judgeor.JudgeImage import JudgeImage
from .judgeor.JudgeNone import JudgeNone
from .judgeor.JudgeOnBuild import JudgeOnBuild
from .judgeor.JudgeRunRun import JudgeRunRun
from .judgeor.JudgeRunUser import JudgeRunUser
from .judgeor.JudgeShellRun import JudgeShellRun
from .judgeor.JudgeUser import JudgeUser
from .judgeor.JudgeVolumeRun import JudgeVolumeRun
from .judgeor.JudgeWorkdirDir import JudgeWorkdirDir
from .judgeor.JudgeWorkdirRun import JudgeWorkdirRun
from .judgeor.JudgeRunWorkdir import JudgeRunWorkdir
from .judgeor.JudgeUserWorkdir import JudgeUserWorkdir
from .judgeor.JudgeDirWorkdir import JudgeDirWorkdir
from typing import List, Tuple

from ..dockerfile_process.preprocess.datatypes.PrimitiveMeta import PrimitiveMeta

instruct_dependency_table = [
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 2, 0, 0, 0, 0, 0, 0, 0, 3, 20, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 4, 5, 5, 5, 6, 7, 7, 5, 5, 5, 0, 5, 0, 0, 0, 0, 0],
    [0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 21, 0, 0, 0, 0, 0, 0, 0],
    [0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 21, 0, 0, 0, 0, 0, 0, 0],
    [0, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 11, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 12, 0, 0, 0, 0, 13, 13, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [15, 14, 15, 15, 15, 16, 17, 17, 15, 15, 15, 16, 15, 15, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 18, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 19, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]
instruct_code_table = {
    "FROM": 0,
    "RUN": 1,
    "LABEL": 2,
    "MAINTAINER": 3,
    "EXPOSE": 4,
    "ENV": 5,
    "ADD": 6,
    "COPY": 7,
    "VOLUME": 8,
    "USER": 9,
    "WORKDIR": 10,
    "ARG": 11,
    "STOPSIGNAL": 12,
    "SHELL": 13,
    "CMD": 14,
    "ENTRYPOINT": 15,
    "ONBUILD": 16,
    "HEALTHCHECK": 17,
}
# TODO: instruct_no_order are generally related to the container runtime phase, not the build phase,
#  and even if there are dependencies, they will not affect the normal build of the container
INSTRUCT_NO_ORDER = ["CMD", "ENTRYPOINT", "ONBUILD", "HEALTHCHECK"]

DICT_DEPENDENCY_TYPE_TRANSFORMER_MODULE_MAPPER = {
    DType.NONE: JudgeNone,
    DType.BASIC_IMAGE: JudgeImage,
    DType.RUN_RUN: JudgeRunRun,
    DType.RUN_USER: JudgeRunUser,
    DType.ENV_RUN: JudgeEnvRun,
    DType.ENV_TUPLE: JudgeEnvTuple,
    DType.ENV_DICT: JudgeEnvDict,
    DType.ENV_DIR: JudgeEnvDir,
    DType.ADD_RUN: JudgeAddRun,
    DType.COPY_RUN: JudgeCopyRun,
    DType.VOLUME_RUN: JudgeVolumeRun,
    DType.BASIC_USER: JudgeUser,
    DType.WORKDIR_RUN: JudgeWorkdirRun,
    DType.WORKDIR_DIR: JudgeWorkdirDir,
    DType.ARG_RUN: JudgeArgRun,
    DType.ARG_TUPLE: JudgeArgTuple,
    DType.ARG_DICT: JudgeArgDict,
    DType.ARG_DIR: JudgeArgDir,
    DType.SHELL_RUN: JudgeShellRun,
    DType.BASIC_ONBUILD: JudgeOnBuild,
    DType.RUN_WORKDIR: JudgeRunWorkdir,
    DType.DIR_WORKDIR: JudgeDirWorkdir,
    DType.USER_WORKDIR: JudgeUserWorkdir  # 已失效
}


def dependency_judge(command_meta1: PrimitiveMeta, command_meta2: PrimitiveMeta) -> Tuple[DDType, str]:
    instruct1_code = instruct_code_table[command_meta1.cmd_name]
    instruct2_code = instruct_code_table[command_meta2.cmd_name]
    dependency_type: DType = DType(instruct_dependency_table[instruct1_code][instruct2_code])

    dependency_class = DICT_DEPENDENCY_TYPE_TRANSFORMER_MODULE_MAPPER[dependency_type]
    preprocess_object = dependency_class(command_meta1, command_meta2)
    return preprocess_object.get_dependence()


def have_instruct_no_order_in_instruct_name_list(name_list: List[str]) -> bool:
    return len(set(name_list) & set(INSTRUCT_NO_ORDER)) != 0
