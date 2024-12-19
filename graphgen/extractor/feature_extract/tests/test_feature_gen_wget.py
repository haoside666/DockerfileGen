import unittest

from graphgen.extractor.util_flag_option import make_arg_simple
from graphgen.extractor.datatypes.BasicDatatypes import Operand
from graphgen.extractor.datatypes.CommandInvocationInitial import CommandInvocationInitial
from graphgen.extractor.datatypes.CommandInvocationWithFeature import CommandInvocationWithFeature
import graphgen.extractor.feature_extract.feature_extract as feature_generation

cmd_name = "wget"


class TestExtractWget(unittest.TestCase):

    def test_wget_1(self) -> None:
        args = []
        operands = [Operand("https://github.com/Kitware/CMake/releases/download/v3.14.0/cmake-3.14.0.tar.gz")]
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

    def test_wget_2(self) -> None:
        args = [make_arg_simple(["-P", "/etc/yum.repos.d/"])]
        operands = [Operand("http://severalnines.com/downloads/cmon/s9s-repo.repo")]
        cmd_inv: CommandInvocationInitial = CommandInvocationInitial(cmd_name, flag_option_list=args,
                                                                     operand_list=operands)

        # Feature Info
        cmd_inv_after_io, feature_info = feature_generation.get_feature_info_from_cmd_invocation(cmd_inv)
        assert feature_info is not None
        cmd_inv_with_feature: CommandInvocationWithFeature = feature_info.apply_feature_info_to_command_invocation(
            cmd_inv_after_io)
        # The former is the expected value and the latter is the actual value
        self.assertEqual(0, len(cmd_inv_with_feature.get_options_with_config_input()))
        self.assertEqual(1, len(cmd_inv_with_feature.get_options_with_config_output()))
        self.assertEqual(1, len(cmd_inv_with_feature.get_operands_with_file()))
        self.assertEqual(0, len(cmd_inv_with_feature.get_operands_with_user()))
        self.assertEqual(0, len(cmd_inv_with_feature.get_operands_with_pkg()))
        self.assertEqual(0, len(cmd_inv_with_feature.get_operands_with_other()))
        print(cmd_inv_with_feature.get_command_feature_info())

    def test_wget_3(self) -> None:
        args = [make_arg_simple(["-q"]),
                make_arg_simple(["-O", "client.zip"])]
        operands = [Operand("https://static2.askmrrobot.com/wowsite/client/AskMrRobotClient-any-1201.zip")]
        cmd_inv: CommandInvocationInitial = CommandInvocationInitial(cmd_name, flag_option_list=args,
                                                                     operand_list=operands)

        # Feature Info
        cmd_inv_after_io, feature_info = feature_generation.get_feature_info_from_cmd_invocation(cmd_inv)
        assert feature_info is not None
        cmd_inv_with_feature: CommandInvocationWithFeature = feature_info.apply_feature_info_to_command_invocation(
            cmd_inv_after_io)
        # The former is the expected value and the latter is the actual value
        self.assertEqual(0, len(cmd_inv_with_feature.get_options_with_config_input()))
        self.assertEqual(1, len(cmd_inv_with_feature.get_options_with_config_output()))
        self.assertEqual(0, len(cmd_inv_with_feature.get_operands_with_file()))
        self.assertEqual(0, len(cmd_inv_with_feature.get_operands_with_user()))
        self.assertEqual(0, len(cmd_inv_with_feature.get_operands_with_pkg()))
        self.assertEqual(0, len(cmd_inv_with_feature.get_operands_with_other()))
        print(cmd_inv_with_feature.get_command_feature_info())

    def test_wget_4(self) -> None:
        args = [make_arg_simple(["--no-cache"]),
                make_arg_simple(["-O", "libnode.so.72"])]
        operands = [Operand("https://cdn.altv.mp/node-module/beta/x64_linux/libnode.so.72")]
        cmd_inv: CommandInvocationInitial = CommandInvocationInitial(cmd_name, flag_option_list=args,
                                                                     operand_list=operands)

        # Feature Info
        cmd_inv_after_io, feature_info = feature_generation.get_feature_info_from_cmd_invocation(cmd_inv)
        assert feature_info is not None
        cmd_inv_with_feature: CommandInvocationWithFeature = feature_info.apply_feature_info_to_command_invocation(
            cmd_inv_after_io)
        # The former is the expected value and the latter is the actual value
        self.assertEqual(0, len(cmd_inv_with_feature.get_options_with_config_input()))
        self.assertEqual(1, len(cmd_inv_with_feature.get_options_with_config_output()))
        self.assertEqual(0, len(cmd_inv_with_feature.get_operands_with_file()))
        self.assertEqual(0, len(cmd_inv_with_feature.get_operands_with_user()))
        self.assertEqual(0, len(cmd_inv_with_feature.get_operands_with_pkg()))
        self.assertEqual(0, len(cmd_inv_with_feature.get_operands_with_other()))
        print(cmd_inv_with_feature.get_command_feature_info())

    def test_wget_5(self) -> None:
        args = [make_arg_simple(["-O", "-"])]
        operands = [Operand("https://cdn.altv.mp/node-module/beta/x64_linux/libnode.so.72")]
        cmd_inv: CommandInvocationInitial = CommandInvocationInitial(cmd_name, flag_option_list=args,
                                                                     operand_list=operands)

        # Feature Info
        cmd_inv_after_io, feature_info = feature_generation.get_feature_info_from_cmd_invocation(cmd_inv)
        assert feature_info is not None
        cmd_inv_with_feature: CommandInvocationWithFeature = feature_info.apply_feature_info_to_command_invocation(
            cmd_inv_after_io)
        # The former is the expected value and the latter is the actual value
        self.assertEqual(0, len(cmd_inv_with_feature.get_options_with_config_input()))
        self.assertEqual(1, len(cmd_inv_with_feature.get_options_with_config_output()))
        self.assertEqual(0, len(cmd_inv_with_feature.get_operands_with_file()))
        self.assertEqual(0, len(cmd_inv_with_feature.get_operands_with_user()))
        self.assertEqual(0, len(cmd_inv_with_feature.get_operands_with_pkg()))
        self.assertEqual(0, len(cmd_inv_with_feature.get_operands_with_other()))
        print(cmd_inv_with_feature.get_command_feature_info())

    def test_wget_6(self) -> None:
        # Test invalid parameters
        args = [make_arg_simple(["-i", "-"])]
        operands = []
        cmd_inv: CommandInvocationInitial = CommandInvocationInitial(cmd_name, flag_option_list=args,
                                                                     operand_list=operands)

        # Feature Info
        cmd_inv_after_io, feature_info = feature_generation.get_feature_info_from_cmd_invocation(cmd_inv)
        assert feature_info is None
