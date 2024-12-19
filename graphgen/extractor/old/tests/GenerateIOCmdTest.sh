#!/bin/bash
#判断参数是否为 0 个
if [ $# == 0 ]; then
  echo "please use ./GenerateIOCmdTest.sh command"
else
    echo "-----------------以下是生成的内容------------------"
    printf 'from typing import List, Optional\n'
    printf 'from extractor.util_flag_option import make_arg_simple\n'
    printf 'from extractor.datatypes.BasicDatatypes import FlagOption, Operand\n'
    printf 'from extractor.datatypes.CommandInvocationInitial import CommandInvocationInitial\n'
    printf 'from extractor.datatypes.CommandInvocationWithIO import CommandInvocationWithIO\n'
    printf 'import extractor.feature_extract.input_and_output_info_extract as feature_generation\n'
    echo
    printf 'cmd_name = "%s"\n' $1
    echo
    echo
    for ((i = 1; i <= 4; i++)); do
      printf 'def test_%s_%s() -> None:\n' $1 ${i}
      printf '    args = []\n'
      printf '    operands = []\n'
      printf '    cmd_inv: CommandInvocationInitial = CommandInvocationInitial(cmd_name, flag_option_list=args, operand_list=operands)\n' $1
      echo
      printf '    # IO Info\n'
      printf '    cmd_inv_after_io, io_info = feature_generation.get_input_output_info_from_cmd_invocation(cmd_inv)\n'
      printf '    assert io_info is not None\n'
      printf '    cmd_inv_with_io: CommandInvocationWithIO = io_info.apply_input_output_info_to_command_invocation(cmd_inv_after_io)\n'
      printf '    assert len(cmd_inv_with_io.get_options_with_config_input()) == 0\n'
      printf '    assert len(cmd_inv_with_io.get_options_with_config_output()) == 0\n'
      printf '    assert len(cmd_inv_with_io.get_operands_with_other_input()) == 0\n'
      printf '    assert len(cmd_inv_with_io.get_operands_with_other_output()) == 0\n'
      printf '    assert cmd_inv_with_io.implicit_use_of_streaming_input is None\n'
      printf '    assert cmd_inv_with_io.implicit_use_of_streaming_output is None\n'
      printf '    print(cmd_inv_with_io.get_command_feature_info())\n'
      echo
      echo
    done
    for ((i = 1; i <= 4; i++)); do
      printf 'test_%s_%s()\n' $1 ${i}
    done
fi
