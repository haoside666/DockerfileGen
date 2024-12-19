import unittest

from graphgen.extractor.util_flag_option import make_arg_simple
from graphgen.extractor.datatypes.BasicDatatypes import Operand
from graphgen.extractor.datatypes.CommandInvocationInitial import CommandInvocationInitial
from graphgen.extractor.datatypes.CommandInvocationWithFeature import CommandInvocationWithFeature
import graphgen.extractor.feature_extract.feature_extract as feature_generation

cmd_name = "groupadd"


class TestExtractGroupAdd(unittest.TestCase):
    def test_groupadd_1(self) -> None:
        args = [make_arg_simple(["-g", "1004"])]
        operands = [Operand("jenkins")]
        cmd_inv: CommandInvocationInitial = CommandInvocationInitial(cmd_name, flag_option_list=args,
                                                                     operand_list=operands)

        # Feature Info
        cmd_inv_after_io, feature_info = feature_generation.get_feature_info_from_cmd_invocation(cmd_inv)
        assert feature_info is not None
        cmd_inv_with_feature: CommandInvocationWithFeature = feature_info.apply_feature_info_to_command_invocation(
            cmd_inv_after_io)
        self.assertEqual(0, len(cmd_inv_with_feature.get_options_with_config_input()))
        self.assertEqual(0, len(cmd_inv_with_feature.get_options_with_config_output()))
        self.assertEqual(0, len(cmd_inv_with_feature.get_operands_with_file()))
        self.assertEqual(1, len(cmd_inv_with_feature.get_operands_with_user()))
        self.assertEqual(0, len(cmd_inv_with_feature.get_operands_with_pkg()))
        self.assertEqual(1, len(cmd_inv_with_feature.get_operands_with_other()))
        print(cmd_inv_with_feature.get_command_feature_info())

    def test_groupadd_2(self) -> None:
        args = [make_arg_simple(["-r"]),
                make_arg_simple(["-g", "433"])]
        operands = [Operand("activemq")]
        cmd_inv: CommandInvocationInitial = CommandInvocationInitial(cmd_name, flag_option_list=args,
                                                                     operand_list=operands)

        # Feature Info
        cmd_inv_after_io, feature_info = feature_generation.get_feature_info_from_cmd_invocation(cmd_inv)
        assert feature_info is not None
        cmd_inv_with_feature: CommandInvocationWithFeature = feature_info.apply_feature_info_to_command_invocation(
            cmd_inv_after_io)
        self.assertEqual(0, len(cmd_inv_with_feature.get_options_with_config_input()))
        self.assertEqual(0, len(cmd_inv_with_feature.get_options_with_config_output()))
        self.assertEqual(0, len(cmd_inv_with_feature.get_operands_with_file()))
        self.assertEqual(1, len(cmd_inv_with_feature.get_operands_with_user()))
        self.assertEqual(0, len(cmd_inv_with_feature.get_operands_with_pkg()))
        self.assertEqual(1, len(cmd_inv_with_feature.get_operands_with_other()))
        print(cmd_inv_with_feature.get_command_feature_info())

    def test_groupadd_3(self) -> None:
        args = []
        operands = [Operand("mysql")]
        cmd_inv: CommandInvocationInitial = CommandInvocationInitial(cmd_name, flag_option_list=args,
                                                                     operand_list=operands)

        # Feature Info
        cmd_inv_after_io, feature_info = feature_generation.get_feature_info_from_cmd_invocation(cmd_inv)
        assert feature_info is not None
        cmd_inv_with_feature: CommandInvocationWithFeature = feature_info.apply_feature_info_to_command_invocation(
            cmd_inv_after_io)
        self.assertEqual(0, len(cmd_inv_with_feature.get_options_with_config_input()))
        self.assertEqual(0, len(cmd_inv_with_feature.get_options_with_config_output()))
        self.assertEqual(0, len(cmd_inv_with_feature.get_operands_with_file()))
        self.assertEqual(1, len(cmd_inv_with_feature.get_operands_with_user()))
        self.assertEqual(0, len(cmd_inv_with_feature.get_operands_with_pkg()))
        self.assertEqual(1, len(cmd_inv_with_feature.get_operands_with_other()))
        print(cmd_inv_with_feature.get_command_feature_info())

    def test_groupadd_4(self) -> None:
        args = [make_arg_simple(["-f"]),
                make_arg_simple(["-g", "2000"])]
        operands = [Operand("conan-2000")]
        cmd_inv: CommandInvocationInitial = CommandInvocationInitial(cmd_name, flag_option_list=args,
                                                                     operand_list=operands)

        # Feature Info
        cmd_inv_after_io, feature_info = feature_generation.get_feature_info_from_cmd_invocation(cmd_inv)
        assert feature_info is not None
        cmd_inv_with_feature: CommandInvocationWithFeature = feature_info.apply_feature_info_to_command_invocation(
            cmd_inv_after_io)
        self.assertEqual(0, len(cmd_inv_with_feature.get_options_with_config_input()))
        self.assertEqual(0, len(cmd_inv_with_feature.get_options_with_config_output()))
        self.assertEqual(0, len(cmd_inv_with_feature.get_operands_with_file()))
        self.assertEqual(1, len(cmd_inv_with_feature.get_operands_with_user()))
        self.assertEqual(0, len(cmd_inv_with_feature.get_operands_with_pkg()))
        self.assertEqual(1, len(cmd_inv_with_feature.get_operands_with_other()))
        print(cmd_inv_with_feature.get_command_feature_info())
