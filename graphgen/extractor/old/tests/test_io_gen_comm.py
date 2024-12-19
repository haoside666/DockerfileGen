from graphgen.extractor.util_flag_option import make_arg_simple
from graphgen.extractor.datatypes.BasicDatatypes import Operand
from graphgen.extractor.datatypes.CommandInvocationInitial import CommandInvocationInitial
from graphgen.extractor import CommandInvocationWithIO
from graphgen.extractor import make_stdout_with_access_stream_output
import graphgen.extractor.old.input_and_output_info_extract as feature_generation

cmd_name = "comm"


def test_comm_1() -> None:
    args = [make_arg_simple(["-1"]), make_arg_simple(["-2"])]
    operands = [Operand("tocomm1.txt"),
                Operand("tocomm2.txt")]

    cmd_inv: CommandInvocationInitial = CommandInvocationInitial(cmd_name, flag_option_list=args, operand_list=operands)

    # IO Info
    cmd_inv_after_io, io_info = feature_generation.get_input_output_info_from_cmd_invocation(cmd_inv)
    assert io_info is not None
    cmd_inv_with_io: CommandInvocationWithIO = io_info.apply_input_output_info_to_command_invocation(cmd_inv_after_io)
    assert len(cmd_inv_with_io.get_options_with_config_input()) == 0
    assert len(cmd_inv_with_io.get_options_with_config_output()) == 0
    assert len(cmd_inv_with_io.get_operands_with_other_input()) == 2
    assert len(cmd_inv_with_io.get_operands_with_other_output()) == 0
    assert cmd_inv_with_io.implicit_use_of_streaming_input is None
    assert cmd_inv_with_io.implicit_use_of_streaming_output == make_stdout_with_access_stream_output()
    print(cmd_inv_with_io.get_command_feature_info())


def test_comm_2() -> None:
    args = []
    # illegal to have more than 2 files to compare
    operands = [Operand("tocomm1.txt"),
                Operand("tocomm2.txt"),
                Operand("tocomm3.txt")]
    cmd_inv: CommandInvocationInitial = CommandInvocationInitial(cmd_name, flag_option_list=args, operand_list=operands)

    # IO Info
    cmd_inv_after_io, io_info = feature_generation.get_input_output_info_from_cmd_invocation(cmd_inv)
    assert io_info is None


test_comm_1()
test_comm_2()
