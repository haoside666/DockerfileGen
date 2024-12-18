import os
import sys
from typing import Optional, Tuple

from dockdepend.extractor.datatypes.CommandInvocationInitial import CommandInvocationInitial
from dockdepend.extractor.datatypes.CommandInvocationAfterIOChange import CommandInvocationAfterIOChange
from dockdepend.extractor import InputOutputInfo

### directory paths
# ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '../../..'))
INPUTOUTPUT_INFO_GENERATORS = "extractor.feature_extract.InputOutputInfo_generators"

DICT_CMD_NAME_TO_REPRESENTATION_IN_MODULE_NAMES = {
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

INPUTOUTPUT_INFO_FILENAME_MODULE_PREFIX = "InputOutputInfoGenerator"
inputoutput_info_generator_prefix_abs = INPUTOUTPUT_INFO_GENERATORS + '.' + INPUTOUTPUT_INFO_FILENAME_MODULE_PREFIX
inputoutput_info_generator_file_module_names = \
    [(inputoutput_info_generator_prefix_abs + name, INPUTOUTPUT_INFO_FILENAME_MODULE_PREFIX + name)
     for name in set(DICT_CMD_NAME_TO_REPRESENTATION_IN_MODULE_NAMES.values())]

for FILENAME_MODULE_PAIR in inputoutput_info_generator_file_module_names:
    FILENAME, MODULE = FILENAME_MODULE_PAIR
    import_str = "from " + FILENAME + " import " + MODULE
    try:
        exec(import_str)
    except ModuleNotFoundError:
        pass  # it's fine if some do not exist, we catch that later


# cannot be merged due to types
def get_input_output_info_from_cmd_invocation(cmd_invocation: CommandInvocationInitial) -> Tuple[
    Optional[CommandInvocationAfterIOChange], Optional[InputOutputInfo]]:
    return get_input_output_info_from_cmd_invocation_in_pipe_mode(cmd_invocation)[:2]


def get_input_output_info_from_cmd_invocation_in_pipe_mode(cmd_invocation: CommandInvocationInitial, pipe: str = "") -> \
        Tuple[Optional[CommandInvocationAfterIOChange], Optional[InputOutputInfo], str]:
    # Get the Generator, info_generator_class_for_cmd_repr, info_generator_class_for_cmd_repr
    info_generator_class_for_cmd_repr = DICT_CMD_NAME_TO_REPRESENTATION_IN_MODULE_NAMES.get(cmd_invocation.cmd_name)
    try:
        info_generator_class_for_cmd = str_to_class(
            str(INPUTOUTPUT_INFO_FILENAME_MODULE_PREFIX) + str(info_generator_class_for_cmd_repr))
        # Initialize the info generator object
        info_generator_object = info_generator_class_for_cmd(cmd_invocation, pipe)
        # Generate info
        info_generator_object.generate_info()
        return info_generator_object.get_cmd_inv_after_io(), info_generator_object.get_info(), info_generator_object.get_pipe()
    except Exception as e:  # module does not exist
        return None, None, pipe


def str_to_class(classname):
    return getattr(sys.modules[__name__], classname)
