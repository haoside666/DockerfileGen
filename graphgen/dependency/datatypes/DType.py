from enum import Enum


class DType(Enum):
    NONE = 0
    BASIC_IMAGE = 1
    RUN_RUN = 2
    RUN_USER = 3
    ENV_RUN = 4
    ENV_TUPLE = 5
    ENV_DICT = 6
    ENV_DIR = 7
    ADD_RUN = 8
    COPY_RUN = 9
    VOLUME_RUN = 10
    BASIC_USER = 11
    WORKDIR_RUN = 12
    WORKDIR_DIR = 13
    ARG_RUN = 14
    ARG_TUPLE = 15
    ARG_DICT = 16
    ARG_DIR = 17
    SHELL_RUN = 18
    BASIC_ONBUILD = 19
    RUN_WORKDIR = 20
    DIR_WORKDIR = 21
    USER_WORKDIR = 22

    # For different stages
    BASIC_MULTI_STAGE = 51
    BASIC_FROM_ONBUILD = 52
