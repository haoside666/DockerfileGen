from typing import List
from dockdepend.extractor.util_flag_option import make_arg_simple
from dockdepend.extractor.datatypes.BasicDatatypes import FlagOption, Operand
from dockdepend.extractor.datatypes.CommandInvocationInitial import CommandInvocationInitial
from dockdepend.extractor import CommandInvocationWithIO
from dockdepend.extractor import make_stdout_with_access_stream_output, \
    make_stdin_with_access_stream_input
import dockdepend.extractor.old.input_and_output_info_extract as feature_generation

cmd_name = "uniq"


def test_uniq_1() -> None:
    args: List[FlagOption] = [make_arg_simple(["-D"])]
    operands: List[Operand] = [Operand("in.txt"),
                               Operand("out.txt")]

    cmd_inv: CommandInvocationInitial = CommandInvocationInitial(cmd_name, flag_option_list=args, operand_list=operands)

    # IO Info
    cmd_inv_after_io, io_info = feature_generation.get_input_output_info_from_cmd_invocation(cmd_inv)
    assert io_info is not None
    cmd_inv_with_io: CommandInvocationWithIO = io_info.apply_input_output_info_to_command_invocation(cmd_inv_after_io)
    assert len(cmd_inv_with_io.get_options_with_config_input()) == 0
    assert len(cmd_inv_with_io.get_options_with_config_output()) == 0
    assert len(cmd_inv_with_io.get_operands_with_other_input()) == 1
    assert len(cmd_inv_with_io.get_operands_with_other_output()) == 1
    assert cmd_inv_with_io.implicit_use_of_streaming_input is None
    assert cmd_inv_with_io.implicit_use_of_streaming_output is None
    print(cmd_inv_with_io.get_command_feature_info())


def test_uniq_2() -> None:
    args: List[FlagOption] = [make_arg_simple(["-c"])]
    operands: List[Operand] = []
    cmd_inv: CommandInvocationInitial = CommandInvocationInitial(cmd_name, flag_option_list=args, operand_list=operands)

    # IO Info
    cmd_inv_after_io, io_info = feature_generation.get_input_output_info_from_cmd_invocation(cmd_inv)
    assert io_info is not None
    cmd_inv_with_io: CommandInvocationWithIO = io_info.apply_input_output_info_to_command_invocation(cmd_inv_after_io)
    assert len(cmd_inv_with_io.get_options_with_config_input()) == 0
    assert len(cmd_inv_with_io.get_options_with_config_output()) == 0
    assert len(cmd_inv_with_io.get_operands_with_other_input()) == 0
    assert len(cmd_inv_with_io.get_operands_with_other_output()) == 0
    assert cmd_inv_with_io.implicit_use_of_streaming_input == make_stdin_with_access_stream_input()
    assert cmd_inv_with_io.implicit_use_of_streaming_output == make_stdout_with_access_stream_output()
    print(cmd_inv_with_io.get_command_feature_info())


def test_uniq_3() -> None:
    args: List[FlagOption] = []
    operands: List[Operand] = [Operand("in.txt"),
                               Operand("out.txt")]
    cmd_inv: CommandInvocationInitial = CommandInvocationInitial(cmd_name, flag_option_list=args, operand_list=operands)

    # IO Info
    cmd_inv_after_io, io_info = feature_generation.get_input_output_info_from_cmd_invocation(cmd_inv)
    assert io_info is not None
    cmd_inv_with_io: CommandInvocationWithIO = io_info.apply_input_output_info_to_command_invocation(cmd_inv_after_io)
    assert len(cmd_inv_with_io.get_options_with_config_input()) == 0
    assert len(cmd_inv_with_io.get_options_with_config_output()) == 0
    assert len(cmd_inv_with_io.get_operands_with_other_input()) == 1
    assert len(cmd_inv_with_io.get_operands_with_other_output()) == 1
    assert cmd_inv_with_io.implicit_use_of_streaming_input is None
    assert cmd_inv_with_io.implicit_use_of_streaming_output is None
    print(cmd_inv_with_io.get_command_feature_info())


test_uniq_1()
test_uniq_2()
test_uniq_3()
