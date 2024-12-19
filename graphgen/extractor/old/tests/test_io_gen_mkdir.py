from graphgen.extractor.util_flag_option import make_arg_simple
from graphgen.extractor.datatypes.BasicDatatypes import Operand
from graphgen.extractor.datatypes.CommandInvocationInitial import CommandInvocationInitial
from graphgen.extractor import CommandInvocationWithIO
import graphgen.extractor.old.input_and_output_info_extract as feature_generation

cmd_name = "mkdir"


def test_mkdir_1() -> None:
    args = []
    operands = [Operand("/app/data")]
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


def test_mkdir_2() -> None:
    args = [make_arg_simple(["-p"])]
    operands = [Operand("/jellyfin"),
                Operand("/media"),
                Operand("/cache")]
    cmd_inv: CommandInvocationInitial = CommandInvocationInitial(cmd_name, flag_option_list=args, operand_list=operands)

    # IO Info
    cmd_inv_after_io, io_info = feature_generation.get_input_output_info_from_cmd_invocation(cmd_inv)
    assert io_info is not None
    cmd_inv_with_io: CommandInvocationWithIO = io_info.apply_input_output_info_to_command_invocation(cmd_inv_after_io)
    assert len(cmd_inv_with_io.get_options_with_config_input()) == 0
    assert len(cmd_inv_with_io.get_options_with_config_output()) == 0
    assert len(cmd_inv_with_io.get_operands_with_other_input()) == 0
    assert len(cmd_inv_with_io.get_operands_with_other_output()) == 3
    assert cmd_inv_with_io.implicit_use_of_streaming_input is None
    assert cmd_inv_with_io.implicit_use_of_streaming_output is None
    print(cmd_inv_with_io.get_command_feature_info())


def test_mkdir_3() -> None:
    args = [make_arg_simple(["-m", "775"]),
            make_arg_simple(["-p"])]
    operands = [Operand("/config/config.d"),
                Operand("/data/film"),
                Operand("/data/games"),
                Operand("/data/music")]
    cmd_inv: CommandInvocationInitial = CommandInvocationInitial(cmd_name, flag_option_list=args, operand_list=operands)

    # IO Info
    cmd_inv_after_io, io_info = feature_generation.get_input_output_info_from_cmd_invocation(cmd_inv)
    assert io_info is not None
    cmd_inv_with_io: CommandInvocationWithIO = io_info.apply_input_output_info_to_command_invocation(cmd_inv_after_io)
    assert len(cmd_inv_with_io.get_options_with_config_input()) == 0
    assert len(cmd_inv_with_io.get_options_with_config_output()) == 0
    assert len(cmd_inv_with_io.get_operands_with_other_input()) == 0
    assert len(cmd_inv_with_io.get_operands_with_other_output()) == 4
    assert cmd_inv_with_io.implicit_use_of_streaming_input is None
    assert cmd_inv_with_io.implicit_use_of_streaming_output is None
    print(cmd_inv_with_io.get_command_feature_info())


def test_mkdir_4() -> None:
    args = [make_arg_simple(["-p"]),
            make_arg_simple(["-v"])]
    operands = [Operand("/root/lib/locale")]
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


test_mkdir_1()
test_mkdir_2()
test_mkdir_3()
test_mkdir_4()
