import unittest

from graphgen.extractor.util_flag_option import make_arg_simple
from graphgen.extractor.datatypes.BasicDatatypes import Operand
from graphgen.extractor.datatypes.CommandInvocationInitial import CommandInvocationInitial
from graphgen.extractor.datatypes.CommandInvocationWithFeature import CommandInvocationWithFeature
import graphgen.extractor.feature_extract.feature_extract as feature_generation

cmd_name = "chmod"


class TestExtractChmod(unittest.TestCase):

    def test_chmod_1(self) -> None:
        args = []
        operands = [Operand("g+rwx"),
                    Operand("/var/run/nginx.pid")]
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
        self.assertEqual(1, len(cmd_inv_with_feature.get_operands_with_file()))
        self.assertEqual(0, len(cmd_inv_with_feature.get_operands_with_user()))
        self.assertEqual(0, len(cmd_inv_with_feature.get_operands_with_pkg()))
        self.assertEqual(0, len(cmd_inv_with_feature.get_operands_with_other()))
        print(cmd_inv_with_feature.get_command_feature_info())

    def test_chmod_2(self) -> None:
        args = []
        operands = [Operand("755"),
                    Operand("/app/webscrapper.py"),
                    Operand("/app/wind_tracker.py"),
                    Operand("/app/telegram_bot.py"),
                    Operand("/app/consts.py"),
                    Operand("/app/windInfo.py")]
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
        self.assertEqual(5, len(cmd_inv_with_feature.get_operands_with_file()))
        self.assertEqual(0, len(cmd_inv_with_feature.get_operands_with_user()))
        self.assertEqual(0, len(cmd_inv_with_feature.get_operands_with_pkg()))
        self.assertEqual(0, len(cmd_inv_with_feature.get_operands_with_other()))
        print(cmd_inv_with_feature.get_command_feature_info())

    def test_chmod_3(self) -> None:
        args = [make_arg_simple(["-R"])]
        operands = [Operand("4775"),
                    Operand("/qbittorrent"),
                    Operand("/Downloads"),
                    Operand("/Downloads/temp")]
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
        self.assertEqual(3, len(cmd_inv_with_feature.get_operands_with_file()))
        self.assertEqual(0, len(cmd_inv_with_feature.get_operands_with_user()))
        self.assertEqual(0, len(cmd_inv_with_feature.get_operands_with_pkg()))
        self.assertEqual(0, len(cmd_inv_with_feature.get_operands_with_other()))
        print(cmd_inv_with_feature.get_command_feature_info())

    def test_chmod_4(self) -> None:
        args = [make_arg_simple(["--reference", "file1.txt"])]
        operands = [Operand("file2.txt")]
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
        self.assertEqual(1, len(cmd_inv_with_feature.get_operands_with_file()))
        self.assertEqual(0, len(cmd_inv_with_feature.get_operands_with_user()))
        self.assertEqual(0, len(cmd_inv_with_feature.get_operands_with_pkg()))
        self.assertEqual(0, len(cmd_inv_with_feature.get_operands_with_other()))
        print(cmd_inv_with_feature.get_command_feature_info())
