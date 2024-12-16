from enum import Enum


# 依赖描述类型
class DDType(Enum):
    NONE = 0  # 无依赖
    BASIC_IMAGE = 1  # Image dependency
    BASIC_USER = 2  # User dependency
    BASIC_ONBUILD = 3  # OnBuild dependency
    RUN_PKG = 4  # have shell pkg intersection
    RUN_IO = 5  # have shell io intersection
    RUN_VAR = 6  # have shell var intersection
    RUN_OTHER = 7  # have shell other intersection
    RUN_USER1 = 8  # shell command user is different from the USER instruction
    RUN_USER2 = 9  # the shell command contains the user in the USER instruction
    ENV_VAR = 10  # environment variable dependencies
    ENV_VAR_IMPLICIT = 11  # system level environment variable dependencies(implicit)
    FILE_DIR = 12  # exist file or directory dependency
    SHELL_RUN = 13  # SHELL instruction dependency
    BOOT = 14  # Boot dependency
    SIDE_EFFECT = 15  # instruction contain side effect command
    UNKNOWN_COMMAND = 16  # instruction has unrecognized command
    CONSISTENCY = 17  # consistency dependency
