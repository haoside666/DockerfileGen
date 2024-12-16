import unittest

from dockdepend.extractor.util_flag_option import make_arg_simple
from dockdepend.extractor.datatypes.BasicDatatypes import Operand
from dockdepend.extractor.datatypes.CommandInvocationInitial import CommandInvocationInitial
from dockdepend.extractor.datatypes.CommandInvocationWithFeature import CommandInvocationWithFeature
import dockdepend.extractor.feature_extract.feature_extract as feature_generation

cmd_name = "useradd"


class TestExtractUseradd(unittest.TestCase):
    def test_useradd_1(self) -> None:
        args = [make_arg_simple(["-m"]),
                make_arg_simple(["-d", "$HOME"])]
        operands = [Operand("user")]
        cmd_inv: CommandInvocationInitial = CommandInvocationInitial(cmd_name, flag_option_list=args,
                                                                     operand_list=operands)

        # Feature Info
        cmd_inv_after_io, feature_info = feature_generation.get_feature_info_from_cmd_invocation(cmd_inv)
        assert feature_info is not None
        cmd_inv_with_feature: CommandInvocationWithFeature = feature_info.apply_feature_info_to_command_invocation(
            cmd_inv_after_io)
        self.assertEqual(0, len(cmd_inv_with_feature.get_options_with_config_input()))
        self.assertEqual(1, len(cmd_inv_with_feature.get_options_with_config_output()))
        self.assertEqual(0, len(cmd_inv_with_feature.get_operands_with_file()))
        self.assertEqual(1, len(cmd_inv_with_feature.get_operands_with_user()))
        self.assertEqual(0, len(cmd_inv_with_feature.get_operands_with_pkg()))
        self.assertEqual(1, len(cmd_inv_with_feature.get_operands_with_other()))
        print(cmd_inv_with_feature.get_command_feature_info())

    def test_useradd_2(self) -> None:
        args = [make_arg_simple(["-m"]),
                make_arg_simple(["-s", "/bin/bash"])]
        operands = [Operand("emundo")]
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

    def test_useradd_3(self) -> None:
        args = [make_arg_simple(["-c", "Emby"]),
                make_arg_simple(["-d", "/usr/lib/emby-server"]),
                make_arg_simple(["-g", "emby"]),
                make_arg_simple(["-m"]),
                make_arg_simple(["-r"])]
        operands = [Operand("emby")]
        cmd_inv: CommandInvocationInitial = CommandInvocationInitial(cmd_name, flag_option_list=args,
                                                                     operand_list=operands)

        # Feature Info
        cmd_inv_after_io, feature_info = feature_generation.get_feature_info_from_cmd_invocation(cmd_inv)
        assert feature_info is not None
        cmd_inv_with_feature: CommandInvocationWithFeature = feature_info.apply_feature_info_to_command_invocation(
            cmd_inv_after_io)
        self.assertEqual(0, len(cmd_inv_with_feature.get_options_with_config_input()))
        self.assertEqual(1, len(cmd_inv_with_feature.get_options_with_config_output()))
        self.assertEqual(0, len(cmd_inv_with_feature.get_operands_with_file()))
        self.assertEqual(1, len(cmd_inv_with_feature.get_operands_with_user()))
        self.assertEqual(0, len(cmd_inv_with_feature.get_operands_with_pkg()))
        self.assertEqual(1, len(cmd_inv_with_feature.get_operands_with_other()))
        print(cmd_inv_with_feature.get_command_feature_info())

    def test_useradd_4(self) -> None:
        args = [make_arg_simple(["-u", "1001"]),
                make_arg_simple(["-G", "www-data"]),
                make_arg_simple(["-d", "/gtrader"]),
                make_arg_simple(["-s", "/bin/bash"]),
                make_arg_simple(["-M"])]
        operands = [Operand("gtrader")]
        cmd_inv: CommandInvocationInitial = CommandInvocationInitial(cmd_name, flag_option_list=args,
                                                                     operand_list=operands)

        # Feature Info
        cmd_inv_after_io, feature_info = feature_generation.get_feature_info_from_cmd_invocation(cmd_inv)
        assert feature_info is not None
        cmd_inv_with_feature: CommandInvocationWithFeature = feature_info.apply_feature_info_to_command_invocation(
            cmd_inv_after_io)
        self.assertEqual(0, len(cmd_inv_with_feature.get_options_with_config_input()))
        self.assertEqual(1, len(cmd_inv_with_feature.get_options_with_config_output()))
        self.assertEqual(0, len(cmd_inv_with_feature.get_operands_with_file()))
        self.assertEqual(1, len(cmd_inv_with_feature.get_operands_with_user()))
        self.assertEqual(0, len(cmd_inv_with_feature.get_operands_with_pkg()))
        self.assertEqual(1, len(cmd_inv_with_feature.get_operands_with_other()))
        print(cmd_inv_with_feature.get_command_feature_info())
