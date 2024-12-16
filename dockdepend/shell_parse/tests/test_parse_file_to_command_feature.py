import unittest

from dockdepend.exception.CustomizedException import ParsingException
from dockdepend.shell_parse.parse import parse_shell_to_feature
import os

CURRENT_DIR = os.path.dirname(__file__)


# Test: Parse various shell script (file format) to command feature structure
# and Get a list of B character types and shell variables to use
class TestASTCmdFeatureParse(unittest.TestCase):
    def test_command_node_parse(self):
        input_script_path = os.path.join(CURRENT_DIR, "data/dockerfile_tests/test_command_node")
        parse_shell_to_feature(input_script_path)

    def test_pipe_node_parse(self):
        input_script_path = os.path.join(CURRENT_DIR, "data/dockerfile_tests/test_pipe_node")
        parse_shell_to_feature(input_script_path)

    def test_if_node_parse(self):
        input_script_path = os.path.join(CURRENT_DIR, "data/dockerfile_tests/test_if_node")
        parse_shell_to_feature(input_script_path)

    def test_while_node_parse(self):
        input_script_path = os.path.join(CURRENT_DIR, "data/dockerfile_tests/test_while_node")
        parse_shell_to_feature(input_script_path)

    def test_for_node_parse(self):
        input_script_path = os.path.join(CURRENT_DIR, "data/dockerfile_tests/test_for_node")
        parse_shell_to_feature(input_script_path)

    def test_fun_node_parse(self):
        input_script_path = os.path.join(CURRENT_DIR, "data/dockerfile_tests/test_fun_node")
        parse_shell_to_feature(input_script_path)

    def test_case_node_parse(self):
        input_script_path = os.path.join(CURRENT_DIR, "data/dockerfile_tests/test_case_node")
        parse_shell_to_feature(input_script_path)

    def test_complex_cmd_parse(self):
        input_script_path = os.path.join(CURRENT_DIR, "data/dockerfile_tests/test_complex_cmd1")
        parse_shell_to_feature(input_script_path)

    def test_dockerfile_run_parse(self):
        input_script_path = os.path.join(CURRENT_DIR, "data/dockerfile_tests/test_dockerfile_run")
        parse_shell_to_feature(input_script_path)

    def test_Vtype_parse(self):
        input_script_path = os.path.join(CURRENT_DIR, "data/dockerfile_tests/Vtype")
        parse_shell_to_feature(input_script_path)

    def test_fail_command_parse(self):
        input_script_path = os.path.join(CURRENT_DIR, "data/dockerfile_tests/test_fail_command")
        # 测试是否抛出ParsingException
        with self.assertRaises(ParsingException):
            parse_shell_to_feature(input_script_path)
        print("test passed!")

    def test_CTLENDQUOTEMARK_parse(self):
        input_script_path = os.path.join(CURRENT_DIR, "data/dockerfile_tests/test_end_of_CTLENDQUOTEMARK")
        parse_shell_to_feature(input_script_path)
