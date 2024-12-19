from graphgen.extractor.util_flag_option import make_arg_simple
from graphgen.extractor.datatypes.BasicDatatypes import Operand
from graphgen.extractor.datatypes.CommandInvocationInitial import CommandInvocationInitial
from graphgen.extractor import CommandInvocationWithIO
import graphgen.extractor.old.input_and_output_info_extract as feature_generation

cmd_name = "tar"


def test_tar_1() -> None:
    args = [make_arg_simple(["-c"]),
            make_arg_simple(["-v"]),
            make_arg_simple(["-f", "/tmp/lo.tar"])]
    operands = [Operand("instdir/")]
    cmd_inv: CommandInvocationInitial = CommandInvocationInitial(cmd_name, flag_option_list=args, operand_list=operands)

    # IO Info
    cmd_inv_after_io, io_info = feature_generation.get_input_output_info_from_cmd_invocation(cmd_inv)
    assert io_info is not None
    cmd_inv_with_io: CommandInvocationWithIO = io_info.apply_input_output_info_to_command_invocation(cmd_inv_after_io)
    assert len(cmd_inv_with_io.get_options_with_config_input()) == 0
    assert len(cmd_inv_with_io.get_options_with_config_output()) == 1
    assert len(cmd_inv_with_io.get_operands_with_other_input()) == 1
    assert len(cmd_inv_with_io.get_operands_with_other_output()) == 0
    assert cmd_inv_with_io.implicit_use_of_streaming_input is None
    assert cmd_inv_with_io.implicit_use_of_streaming_output is None
    print(cmd_inv_with_io.get_command_feature_info())


def test_tar_2() -> None:
    args = [make_arg_simple(["-c"]),
            make_arg_simple(["-v"]),
            make_arg_simple(["-f", "myarchive.tar"]),
            make_arg_simple(["-C", "/mydata"])]
    operands = [Operand("file1"), Operand("file2")]
    cmd_inv: CommandInvocationInitial = CommandInvocationInitial(cmd_name, flag_option_list=args, operand_list=operands)

    # IO Info
    cmd_inv_after_io, io_info = feature_generation.get_input_output_info_from_cmd_invocation(cmd_inv)
    assert io_info is not None
    cmd_inv_with_io: CommandInvocationWithIO = io_info.apply_input_output_info_to_command_invocation(cmd_inv_after_io)
    assert len(cmd_inv_with_io.get_options_with_config_input()) == 1
    assert len(cmd_inv_with_io.get_options_with_config_output()) == 1
    assert len(cmd_inv_with_io.get_operands_with_other_input()) == 2
    assert len(cmd_inv_with_io.get_operands_with_other_output()) == 0
    assert cmd_inv_with_io.implicit_use_of_streaming_input is None
    assert cmd_inv_with_io.implicit_use_of_streaming_output is None
    print(cmd_inv_with_io.get_command_feature_info())


def test_tar_3() -> None:
    args = [make_arg_simple(["-z"]),
            make_arg_simple(["-x"]),
            make_arg_simple(["-v"]),
            make_arg_simple(["-f", "gromacs-2018.3.tar.gz"])]
    operands = []
    cmd_inv: CommandInvocationInitial = CommandInvocationInitial(cmd_name, flag_option_list=args, operand_list=operands)

    # IO Info
    cmd_inv_after_io, io_info = feature_generation.get_input_output_info_from_cmd_invocation(cmd_inv)
    assert io_info is not None
    cmd_inv_with_io: CommandInvocationWithIO = io_info.apply_input_output_info_to_command_invocation(cmd_inv_after_io)
    assert len(cmd_inv_with_io.get_options_with_config_input()) == 1
    assert len(cmd_inv_with_io.get_options_with_config_output()) == 0
    assert len(cmd_inv_with_io.get_operands_with_other_input()) == 0
    assert len(cmd_inv_with_io.get_operands_with_other_output()) == 1
    assert cmd_inv_with_io.implicit_use_of_streaming_input is None
    assert cmd_inv_with_io.implicit_use_of_streaming_output is None
    print(cmd_inv_with_io.get_command_feature_info())


def test_tar_4() -> None:
    args = [make_arg_simple(["-x"]),
            make_arg_simple(["-z"]),
            make_arg_simple(["-f", "/home/hugo.tar.gz"]),
            make_arg_simple(["-C", "/home"])]
    operands = []
    cmd_inv: CommandInvocationInitial = CommandInvocationInitial(cmd_name, flag_option_list=args, operand_list=operands)

    # IO Info
    cmd_inv_after_io, io_info = feature_generation.get_input_output_info_from_cmd_invocation(cmd_inv)
    assert io_info is not None
    cmd_inv_with_io: CommandInvocationWithIO = io_info.apply_input_output_info_to_command_invocation(cmd_inv_after_io)
    assert len(cmd_inv_with_io.get_options_with_config_input()) == 1
    assert len(cmd_inv_with_io.get_options_with_config_output()) == 1
    assert len(cmd_inv_with_io.get_operands_with_other_input()) == 0
    assert len(cmd_inv_with_io.get_operands_with_other_output()) == 1
    assert cmd_inv_with_io.implicit_use_of_streaming_input is None
    assert cmd_inv_with_io.implicit_use_of_streaming_output is None
    print(cmd_inv_with_io.get_command_feature_info())


def test_tar_5() -> None:
    args = [make_arg_simple(["-c"]),
            make_arg_simple(["-z"]),
            make_arg_simple(["-v"]),
            make_arg_simple(["-f", "archive.tar.gz"])]
    operands = [Operand("file1.txt"), Operand("file2.txt"), Operand("directory1"), Operand("directory2")]
    cmd_inv: CommandInvocationInitial = CommandInvocationInitial(cmd_name, flag_option_list=args, operand_list=operands)

    # IO Info
    cmd_inv_after_io, io_info = feature_generation.get_input_output_info_from_cmd_invocation(cmd_inv)
    assert io_info is not None
    cmd_inv_with_io: CommandInvocationWithIO = io_info.apply_input_output_info_to_command_invocation(cmd_inv_after_io)
    assert len(cmd_inv_with_io.get_options_with_config_input()) == 0
    assert len(cmd_inv_with_io.get_options_with_config_output()) == 1
    assert len(cmd_inv_with_io.get_operands_with_other_input()) == 4
    assert len(cmd_inv_with_io.get_operands_with_other_output()) == 0
    assert cmd_inv_with_io.implicit_use_of_streaming_input is None
    assert cmd_inv_with_io.implicit_use_of_streaming_output is None
    print(cmd_inv_with_io.get_command_feature_info())


def test_tar_6() -> None:
    args = [make_arg_simple(["-x"]),
            make_arg_simple(["-C", "/usr/local"])]
    operands = []
    cmd_inv: CommandInvocationInitial = CommandInvocationInitial(cmd_name, flag_option_list=args, operand_list=operands)

    # IO Info
    pipe = "sbt-1.2.8.tgz"
    cmd_inv_after_io, io_info, pipe = feature_generation.get_input_output_info_from_cmd_invocation_in_pipe_mode(cmd_inv,
                                                                                                                pipe)
    assert io_info is not None
    cmd_inv_with_io: CommandInvocationWithIO = io_info.apply_input_output_info_to_command_invocation(cmd_inv_after_io)
    assert len(cmd_inv_with_io.get_options_with_config_input()) == 0
    assert len(cmd_inv_with_io.get_options_with_config_output()) == 1
    assert len(cmd_inv_with_io.get_operands_with_other_input()) == 0
    assert len(cmd_inv_with_io.get_operands_with_other_output()) == 1
    assert cmd_inv_with_io.implicit_use_of_streaming_input is None
    assert cmd_inv_with_io.implicit_use_of_streaming_output is None
    assert pipe == "/usr/local/sbt-1.2.8"
    print(cmd_inv_with_io.get_command_feature_info())


def test_tar_7() -> None:
    args = [make_arg_simple(["-x"]),
            make_arg_simple(["-z"]),
            make_arg_simple(["-f", "-"])]
    operands = []
    cmd_inv: CommandInvocationInitial = CommandInvocationInitial(cmd_name, flag_option_list=args, operand_list=operands)

    # IO Info
    pipe = "edirect.tar.gz"
    cmd_inv_after_io, io_info, pipe = feature_generation.get_input_output_info_from_cmd_invocation_in_pipe_mode(cmd_inv,
                                                                                                                pipe)
    assert io_info is not None
    cmd_inv_with_io: CommandInvocationWithIO = io_info.apply_input_output_info_to_command_invocation(cmd_inv_after_io)
    assert len(cmd_inv_with_io.get_options_with_config_input()) == 1
    assert len(cmd_inv_with_io.get_options_with_config_output()) == 0
    assert len(cmd_inv_with_io.get_operands_with_other_input()) == 0
    assert len(cmd_inv_with_io.get_operands_with_other_output()) == 1
    assert cmd_inv_with_io.implicit_use_of_streaming_input is None
    assert cmd_inv_with_io.implicit_use_of_streaming_output is None
    assert pipe == "edirect"
    print(cmd_inv_with_io.get_command_feature_info())


# test_tar_1()
# test_tar_2()
# test_tar_3()
# test_tar_4()
# test_tar_5()
# test_tar_6()
test_tar_7()
