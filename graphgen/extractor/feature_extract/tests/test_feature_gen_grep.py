import unittest

from graphgen.extractor.util_flag_option import make_arg_simple
from graphgen.extractor.datatypes.BasicDatatypes import Operand
from graphgen.extractor.datatypes.CommandInvocationInitial import CommandInvocationInitial
from graphgen.extractor.datatypes.CommandInvocationWithFeature import CommandInvocationWithFeature
import graphgen.extractor.feature_extract.feature_extract as feature_generation

cmd_name = "grep"


class TestExtractGrep(unittest.TestCase):

    def test_grep_1(self) -> None:
        args = [make_arg_simple(["-L"]), make_arg_simple(["-f", "-"])]
        operands = [Operand("in1.txt"),
                    Operand("in2.txt")]
        cmd_inv: CommandInvocationInitial = CommandInvocationInitial(cmd_name, flag_option_list=args,
                                                                     operand_list=operands)

        # Feature Info
        cmd_inv_after_io, feature_info = feature_generation.get_feature_info_from_cmd_invocation(cmd_inv)
        assert feature_info is not None
        cmd_inv_with_feature: CommandInvocationWithFeature = feature_info.apply_feature_info_to_command_invocation(
            cmd_inv_after_io)
        # The former is the expected value and the latter is the actual value
        self.assertEqual(1, len(cmd_inv_with_feature.get_options_with_config_input()))
        self.assertEqual(0, len(cmd_inv_with_feature.get_options_with_config_output()))
        self.assertEqual(2, len(cmd_inv_with_feature.get_operands_with_file()))
        self.assertEqual(0, len(cmd_inv_with_feature.get_operands_with_user()))
        self.assertEqual(0, len(cmd_inv_with_feature.get_operands_with_pkg()))
        self.assertEqual(0, len(cmd_inv_with_feature.get_operands_with_other()))
        print(cmd_inv_with_feature.get_command_feature_info())

    def test_grep_2(self) -> None:
        args = [make_arg_simple(["-f", "dict.txt"]),
                make_arg_simple(["-e", "*"]),
                make_arg_simple(["-b"])]
        operands = [Operand("in1.txt"),
                    Operand("in2.txt")]
        cmd_inv: CommandInvocationInitial = CommandInvocationInitial(cmd_name, flag_option_list=args,
                                                                     operand_list=operands)

        # Feature Info
        cmd_inv_after_io, feature_info = feature_generation.get_feature_info_from_cmd_invocation(cmd_inv)
        assert feature_info is not None
        cmd_inv_with_feature: CommandInvocationWithFeature = feature_info.apply_feature_info_to_command_invocation(
            cmd_inv_after_io)
        # The former is the expected value and the latter is the actual value
        self.assertEqual(1, len(cmd_inv_with_feature.get_options_with_config_input()))
        self.assertEqual(0, len(cmd_inv_with_feature.get_options_with_config_output()))
        self.assertEqual(2, len(cmd_inv_with_feature.get_operands_with_file()))
        self.assertEqual(0, len(cmd_inv_with_feature.get_operands_with_user()))
        self.assertEqual(0, len(cmd_inv_with_feature.get_operands_with_pkg()))
        self.assertEqual(0, len(cmd_inv_with_feature.get_operands_with_other()))
        print(cmd_inv_with_feature.get_command_feature_info())

    def test_grep_3(self) -> None:
        args = [make_arg_simple(["-f", "dict.txt"]),
                make_arg_simple(["-e", "*"]),
                make_arg_simple(["-f", "dict2.txt"])]
        operands = [Operand("in1.txt"),
                    Operand("-")]
        cmd_inv: CommandInvocationInitial = CommandInvocationInitial(cmd_name, flag_option_list=args,
                                                                     operand_list=operands)

        # Feature Info
        cmd_inv_after_io, feature_info = feature_generation.get_feature_info_from_cmd_invocation(cmd_inv)
        assert feature_info is not None
        cmd_inv_with_feature: CommandInvocationWithFeature = feature_info.apply_feature_info_to_command_invocation(
            cmd_inv_after_io)
        # The former is the expected value and the latter is the actual value
        self.assertEqual(2, len(cmd_inv_with_feature.get_options_with_config_input()))
        self.assertEqual(0, len(cmd_inv_with_feature.get_options_with_config_output()))
        self.assertEqual(2, len(cmd_inv_with_feature.get_operands_with_file()))
        self.assertEqual(0, len(cmd_inv_with_feature.get_operands_with_user()))
        self.assertEqual(0, len(cmd_inv_with_feature.get_operands_with_pkg()))
        self.assertEqual(0, len(cmd_inv_with_feature.get_operands_with_other()))
        print(cmd_inv_with_feature.get_command_feature_info())

    def test_grep_4(self) -> None:
        args = [make_arg_simple(["-f", "dict.txt"]),
                make_arg_simple(["-e", "*"]),
                make_arg_simple(["-f", "dict2.txt"]),
                make_arg_simple(["-n"]),
                make_arg_simple(["-b"])]
        operands = [Operand("in1.txt"),
                    Operand("in2.txt"),
                    Operand("in3.txt")]
        cmd_inv: CommandInvocationInitial = CommandInvocationInitial(cmd_name, flag_option_list=args,
                                                                     operand_list=operands)

        # Feature Info
        cmd_inv_after_io, feature_info = feature_generation.get_feature_info_from_cmd_invocation(cmd_inv)
        assert feature_info is not None
        cmd_inv_with_feature: CommandInvocationWithFeature = feature_info.apply_feature_info_to_command_invocation(
            cmd_inv_after_io)
        # The former is the expected value and the latter is the actual value
        self.assertEqual(2, len(cmd_inv_with_feature.get_options_with_config_input()))
        self.assertEqual(0, len(cmd_inv_with_feature.get_options_with_config_output()))
        self.assertEqual(3, len(cmd_inv_with_feature.get_operands_with_file()))
        self.assertEqual(0, len(cmd_inv_with_feature.get_operands_with_user()))
        self.assertEqual(0, len(cmd_inv_with_feature.get_operands_with_pkg()))
        self.assertEqual(0, len(cmd_inv_with_feature.get_operands_with_other()))
        print(cmd_inv_with_feature.get_command_feature_info())

    def test_grep_5(self) -> None:
        args = [make_arg_simple(["-q"]), make_arg_simple(["-s"])]
        operands = [Operand("*"),
                    Operand("in1.txt"),
                    Operand("in2.txt")]
        cmd_inv: CommandInvocationInitial = CommandInvocationInitial(cmd_name, flag_option_list=args,
                                                                     operand_list=operands)

        # Feature Info
        cmd_inv_after_io, feature_info = feature_generation.get_feature_info_from_cmd_invocation(cmd_inv)
        assert feature_info is not None
        cmd_inv_with_feature: CommandInvocationWithFeature = feature_info.apply_feature_info_to_command_invocation(
            cmd_inv_after_io)
        # The former is the expected value and the latter is the actual value
        self.assertEqual(0, len(cmd_inv_with_feature.get_options_with_config_input()))
        self.assertEqual(0, len(cmd_inv_with_feature.get_options_with_config_output()))
        self.assertEqual(2, len(cmd_inv_with_feature.get_operands_with_file()))
        self.assertEqual(0, len(cmd_inv_with_feature.get_operands_with_user()))
        self.assertEqual(0, len(cmd_inv_with_feature.get_operands_with_pkg()))
        self.assertEqual(0, len(cmd_inv_with_feature.get_operands_with_other()))
        print(cmd_inv_with_feature.get_command_feature_info())
