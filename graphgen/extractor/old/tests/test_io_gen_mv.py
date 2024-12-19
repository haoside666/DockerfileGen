from typing import List
from graphgen.extractor.util_flag_option import make_arg_simple
from graphgen.extractor.datatypes.BasicDatatypes import FlagOption, Operand
from graphgen.extractor.datatypes.CommandInvocationInitial import CommandInvocationInitial
from graphgen.extractor import CommandInvocationWithIO
import graphgen.extractor.old.input_and_output_info_extract as feature_generation

cmd_name = "mv"


def test_mv_1() -> None:
    args = []
    operands = [Operand("*.pl"),
                Operand("bin/.")]
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


def test_mv_2() -> None:
    args: List[FlagOption] = [make_arg_simple(["-t", "dest"])]
    operands: List[Operand] = [Operand("tomove1.txt"),
                               Operand("tomove2.txt")]
    cmd_inv: CommandInvocationInitial = CommandInvocationInitial(cmd_name, flag_option_list=args, operand_list=operands)

    # IO Info
    cmd_inv_after_io, io_info = feature_generation.get_input_output_info_from_cmd_invocation(cmd_inv)
    assert io_info is not None
    cmd_inv_with_io: CommandInvocationWithIO = io_info.apply_input_output_info_to_command_invocation(cmd_inv_after_io)
    assert len(cmd_inv_with_io.get_options_with_config_input()) == 0
    assert len(cmd_inv_with_io.get_options_with_config_output()) == 1
    assert len(cmd_inv_with_io.get_operands_with_other_input()) == 2
    assert len(cmd_inv_with_io.get_operands_with_other_output()) == 0
    assert cmd_inv_with_io.implicit_use_of_streaming_input is None
    assert cmd_inv_with_io.implicit_use_of_streaming_output is None
    print(cmd_inv_with_io.get_command_feature_info())


def test_mv_3() -> None:
    args: List[FlagOption] = [make_arg_simple(["-v"])]
    operands: List[Operand] = [Operand("tomove1.txt"),
                               Operand("tomove2.txt"),
                               Operand("dest")]
    cmd_inv: CommandInvocationInitial = CommandInvocationInitial(cmd_name, flag_option_list=args, operand_list=operands)
    # cmd_inv_pref: CommandInvocationPrefix = CommandInvocationPrefix(cmd_inv.cmd_name, cmd_inv.flag_option_list, [])

    # IO Info
    cmd_inv_after_io, io_info = feature_generation.get_input_output_info_from_cmd_invocation(cmd_inv)
    assert io_info is not None
    cmd_inv_with_io: CommandInvocationWithIO = io_info.apply_input_output_info_to_command_invocation(cmd_inv_after_io)
    assert len(cmd_inv_with_io.get_options_with_config_input()) == 0
    assert len(cmd_inv_with_io.get_options_with_config_output()) == 0
    assert len(cmd_inv_with_io.get_operands_with_other_input()) == 2
    assert len(cmd_inv_with_io.get_operands_with_other_output()) == 1
    assert cmd_inv_with_io.implicit_use_of_streaming_input is None
    assert cmd_inv_with_io.implicit_use_of_streaming_output is None
    print(cmd_inv_with_io.get_command_feature_info())


def test_mv_4() -> None:
    args = [make_arg_simple(["-t", "/usr/bin/frps"])]
    operands = [Operand("/frp_0.31.2_linux_amd64/frps"),
                Operand("/usr/bin/frps"),
                Operand("/frp_0.31.2_linux_amd64/frps.ini")]
    cmd_inv: CommandInvocationInitial = CommandInvocationInitial(cmd_name, flag_option_list=args, operand_list=operands)

    # IO Info
    cmd_inv_after_io, io_info = feature_generation.get_input_output_info_from_cmd_invocation(cmd_inv)
    assert io_info is not None
    cmd_inv_with_io: CommandInvocationWithIO = io_info.apply_input_output_info_to_command_invocation(cmd_inv_after_io)
    assert len(cmd_inv_with_io.get_options_with_config_input()) == 0
    assert len(cmd_inv_with_io.get_options_with_config_output()) == 1
    assert len(cmd_inv_with_io.get_operands_with_other_input()) == 3
    assert len(cmd_inv_with_io.get_operands_with_other_output()) == 0
    assert cmd_inv_with_io.implicit_use_of_streaming_input is None
    assert cmd_inv_with_io.implicit_use_of_streaming_output is None
    print(cmd_inv_with_io.get_command_feature_info())


test_mv_1()
test_mv_2()
test_mv_3()
test_mv_4()
