from graphgen.extractor.util_flag_option import make_arg_simple
from graphgen.extractor.datatypes.BasicDatatypes import Operand
from graphgen.extractor.datatypes.CommandInvocationInitial import CommandInvocationInitial
from graphgen.extractor import CommandInvocationWithIO
import graphgen.extractor.old.input_and_output_info_extract as feature_generation

cmd_name = "wget"


def test_wget_1() -> None:
    args = []
    operands = [Operand("https://github.com/Kitware/CMake/releases/download/v3.14.0/cmake-3.14.0.tar.gz")]
    cmd_inv: CommandInvocationInitial = CommandInvocationInitial(cmd_name, flag_option_list=args, operand_list=operands)

    # IO Info
    cmd_inv_after_io, io_info = feature_generation.get_input_output_info_from_cmd_invocation(cmd_inv)
    assert io_info is not None
    cmd_inv_with_io: CommandInvocationWithIO = io_info.apply_input_output_info_to_command_invocation(cmd_inv_after_io)
    assert len(cmd_inv_with_io.get_options_with_config_input()) == 0
    assert len(cmd_inv_with_io.get_options_with_config_output()) == 0
    assert len(cmd_inv_with_io.get_operands_with_other_input()) == 0
    assert len(cmd_inv_with_io.get_operands_with_other_output()) == 1
    assert cmd_inv_with_io.implicit_use_of_streaming_input is None
    assert cmd_inv_with_io.implicit_use_of_streaming_output is None
    print(cmd_inv_with_io.get_command_feature_info())


def test_wget_2() -> None:
    args = [make_arg_simple(["-P", "/etc/yum.repos.d/"])]
    operands = [Operand("http://severalnines.com/downloads/cmon/s9s-repo.repo")]
    cmd_inv: CommandInvocationInitial = CommandInvocationInitial(cmd_name, flag_option_list=args, operand_list=operands)

    # IO Info
    cmd_inv_after_io, io_info = feature_generation.get_input_output_info_from_cmd_invocation(cmd_inv)
    assert io_info is not None
    cmd_inv_with_io: CommandInvocationWithIO = io_info.apply_input_output_info_to_command_invocation(cmd_inv_after_io)
    assert len(cmd_inv_with_io.get_options_with_config_input()) == 0
    assert len(cmd_inv_with_io.get_options_with_config_output()) == 1
    assert len(cmd_inv_with_io.get_operands_with_other_input()) == 0
    assert len(cmd_inv_with_io.get_operands_with_other_output()) == 1
    assert cmd_inv_with_io.implicit_use_of_streaming_input is None
    assert cmd_inv_with_io.implicit_use_of_streaming_output is None
    print(cmd_inv_with_io.get_command_feature_info())


def test_wget_3() -> None:
    args = [make_arg_simple(["-q"]),
            make_arg_simple(["-O", "client.zip"])]
    operands = [Operand("https://static2.askmrrobot.com/wowsite/client/AskMrRobotClient-any-1201.zip")]
    cmd_inv: CommandInvocationInitial = CommandInvocationInitial(cmd_name, flag_option_list=args, operand_list=operands)

    # IO Info
    cmd_inv_after_io, io_info = feature_generation.get_input_output_info_from_cmd_invocation(cmd_inv)
    assert io_info is not None
    cmd_inv_with_io: CommandInvocationWithIO = io_info.apply_input_output_info_to_command_invocation(cmd_inv_after_io)
    assert len(cmd_inv_with_io.get_options_with_config_input()) == 0
    assert len(cmd_inv_with_io.get_options_with_config_output()) == 1
    assert len(cmd_inv_with_io.get_operands_with_other_input()) == 0
    assert len(cmd_inv_with_io.get_operands_with_other_output()) == 0
    assert cmd_inv_with_io.implicit_use_of_streaming_input is None
    assert cmd_inv_with_io.implicit_use_of_streaming_output is None
    print(cmd_inv_with_io.get_command_feature_info())


def test_wget_4() -> None:
    args = [make_arg_simple(["--no-cache"]),
            make_arg_simple(["-O", "libnode.so.72"])]
    operands = [Operand("https://cdn.altv.mp/node-module/beta/x64_linux/libnode.so.72")]
    cmd_inv: CommandInvocationInitial = CommandInvocationInitial(cmd_name, flag_option_list=args, operand_list=operands)

    # IO Info
    cmd_inv_after_io, io_info = feature_generation.get_input_output_info_from_cmd_invocation(cmd_inv)
    assert io_info is not None
    cmd_inv_with_io: CommandInvocationWithIO = io_info.apply_input_output_info_to_command_invocation(cmd_inv_after_io)
    assert len(cmd_inv_with_io.get_options_with_config_input()) == 0
    assert len(cmd_inv_with_io.get_options_with_config_output()) == 1
    assert len(cmd_inv_with_io.get_operands_with_other_input()) == 0
    assert len(cmd_inv_with_io.get_operands_with_other_output()) == 0
    assert cmd_inv_with_io.implicit_use_of_streaming_input is None
    assert cmd_inv_with_io.implicit_use_of_streaming_output is None
    print(cmd_inv_with_io.get_command_feature_info())


def test_wget_5() -> None:
    args = [make_arg_simple(["-O", "-"])]
    operands = [Operand("https://cdn.altv.mp/node-module/beta/x64_linux/libnode.so.72")]
    cmd_inv: CommandInvocationInitial = CommandInvocationInitial(cmd_name, flag_option_list=args, operand_list=operands)

    # IO Info
    cmd_inv_after_io, io_info, pipe = feature_generation.get_input_output_info_from_cmd_invocation_in_pipe_mode(cmd_inv)
    assert io_info is not None
    cmd_inv_with_io: CommandInvocationWithIO = io_info.apply_input_output_info_to_command_invocation(cmd_inv_after_io)
    assert len(cmd_inv_with_io.get_options_with_config_input()) == 0
    assert len(cmd_inv_with_io.get_options_with_config_output()) == 1
    assert len(cmd_inv_with_io.get_operands_with_other_input()) == 0
    assert len(cmd_inv_with_io.get_operands_with_other_output()) == 0
    assert cmd_inv_with_io.implicit_use_of_streaming_input is None
    assert cmd_inv_with_io.implicit_use_of_streaming_output is None
    assert pipe == "libnode.so.72"
    print(cmd_inv_with_io.get_command_feature_info())


def test_wget_6() -> None:
    args = [make_arg_simple(["-i", "-"])]
    operands = []
    cmd_inv: CommandInvocationInitial = CommandInvocationInitial(cmd_name, flag_option_list=args, operand_list=operands)

    # IO Info
    pipe = "latest"
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
    assert pipe == "latest"
    print(cmd_inv_with_io.get_command_feature_info())


test_wget_1()
test_wget_2()
test_wget_3()
test_wget_4()
test_wget_5()
test_wget_6()
