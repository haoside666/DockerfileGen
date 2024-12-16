import importlib
import os
import sys
from typing import Optional, Tuple

from dockdepend.extractor.datatypes.CommandInvocationInitial import CommandInvocationInitial
from dockdepend.extractor.datatypes.CommandInvocationAfterIOChange import CommandInvocationAfterIOChange
from dockdepend.extractor.feature_extract.datatypes.FeatureInfo import FeatureInfo

### directory paths
FEATURE_INFO_GENERATORS = f"{__name__.rsplit('.', maxsplit=1)[0]}.FeatureInfo_generators"

DICT_CMD_NAME_TO_REPRESENTATION_IN_MODULE_NAMES = {
    "apk": "Apk",
    "apt": "Apt",
    "apt-get": "Apt",
    "bundle": "Bundle",
    "cargo": "Cargo",
    "chown": "Chown",
    "composer": "Composer",
    "default": "Default",
    "docker-php-ext-install": "DockerPhp",
    "dpkg": "Dpkg",
    "gem": "Gem",
    "git": "Git",
    "go": "Go",
    "gradle": "Gradle",
    "groupadd": "Groupadd",
    "addgroup": "Groupadd",
    "groupdel": "Groupdel",
    "delgroup": "Groupdel",
    "ifcond": "Ifcond",
    "useradd": "Useradd",
    "adduser": "Useradd",
    "userdel": "Userdel",
    "deluser": "Userdel",
    "dnf": "Yum",
    "make": "Make",
    "mvn": "Mvn",
    "node": "Node",
    "npm": "Npm",
    "pnpm": "Npm",
    "pacman": "Pacman",
    "pecl": "Pecl",
    "php": "Php",
    "pip": "Pip",
    "pip3": "Pip",
    "python": "Python",
    "python3": "Python",
    "swift": "Swift",
    "xargs": "Xargs",
    "yum": "Yum",
    "yarn": "Yarn",
    "zypper": "Zypper",
    "awk": "Awk",
    "cat": "Cat",
    "chmod": "Chmod",
    "col": "Col",
    "comm": "Comm",
    "cp": "Cp",
    "curl": "Curl",
    "cut": "Cut",
    "diff": "Diff",
    "echo": "Echo",
    "printf": "Echo",
    "grep": "Grep",
    "head": "Head",
    "ln": "Ln",
    "mkdir": "Mkdir",
    "mkfifo": "Mkfifo",
    "mv": "Mv",
    "rm": "Rm",
    "sed": "Sed",
    "seq": "Seq",
    "sort": "Sort",
    "tail": "Tail",
    "tar": "Tar",
    "tee": "Tee",
    "tr": "Tr",
    "uniq": "Uniq",
    "unzip": "Unzip",
    "wc": "Wc",
    "wget": "Wget"
}

FEATURE_INFO_FILENAME_MODULE_PREFIX = "FeatureInfoGenerator"
feature_info_generator_prefix_abs = FEATURE_INFO_GENERATORS + '.' + FEATURE_INFO_FILENAME_MODULE_PREFIX
feature_info_generator_file_module_names = \
    [(feature_info_generator_prefix_abs + name, FEATURE_INFO_FILENAME_MODULE_PREFIX + name)
     for name in set(DICT_CMD_NAME_TO_REPRESENTATION_IN_MODULE_NAMES.values())]

for FILENAME_MODULE_PAIR in feature_info_generator_file_module_names:
    FILENAME, MODULE = FILENAME_MODULE_PAIR
    import_str = "from " + FILENAME + " import " + MODULE
    try:
        exec(import_str)
    except ModuleNotFoundError as e:
        print(e.args[0], file=sys.stderr)
        pass  # it's fine if some do not exist, we catch that later


# cannot be merged due to types
def get_feature_info_from_cmd_invocation(cmd_invocation: CommandInvocationInitial) -> Tuple[
    Optional[CommandInvocationAfterIOChange], Optional[FeatureInfo]]:
    return get_feature_info_from_cmd_invocation_in_pipe_mode(cmd_invocation)[:2]


def get_feature_info_from_cmd_invocation_in_pipe_mode(cmd_invocation: CommandInvocationInitial, pipe: str = "") -> \
        Tuple[Optional[CommandInvocationAfterIOChange], Optional[FeatureInfo], str]:
    # Get the Generator, info_generator_class_for_cmd_repr, info_generator_class_for_cmd_repr
    info_generator_class_for_cmd_repr = DICT_CMD_NAME_TO_REPRESENTATION_IN_MODULE_NAMES.get(cmd_invocation.cmd_name,
                                                                                            "Default")
    try:
        info_generator_class_for_cmd = str_to_class(
            str(FEATURE_INFO_FILENAME_MODULE_PREFIX) + str(info_generator_class_for_cmd_repr))
        # Initialize the info generator object
        info_generator_object = info_generator_class_for_cmd(cmd_invocation, pipe)
        # Generate info
        info_generator_object.generate_info()
        return info_generator_object.get_cmd_inv_after_io(), info_generator_object.get_info(), info_generator_object.get_pipe()
    except Exception as e:
        return None, None, pipe


def str_to_class(classname):
    return getattr(sys.modules[__name__], classname)
