import unittest

from dockdepend.exception.CustomizedException import ParsingException
from dockdepend.shell_parse.parse import parse_shell_script_file_to_instruct_feature
import os

CURRENT_DIR = os.path.dirname(__file__)


# Test: Parse various shell script (file format) to command feature structure
# and Get a list of B character types and shell variables to use
class TestASTCmdFeatureParse(unittest.TestCase):
    def test_parse_shell_script1(self):
        input_script_path = os.path.join(CURRENT_DIR, "data/shell_tests/for_spaces.sh")
        print(parse_shell_script_file_to_instruct_feature(input_script_path))

    def test_parse_shell_script2(self):
        input_script_path = os.path.join(CURRENT_DIR, "data/shell_tests/grade.sh")
        print(parse_shell_script_file_to_instruct_feature(input_script_path))

    def test_parse_shell_script3(self):
        input_script_path = os.path.join(CURRENT_DIR, "data/shell_tests/send_emails.sh")
        print(parse_shell_script_file_to_instruct_feature(input_script_path))

    def test_parse_shell_script4(self):
        input_script_path = os.path.join(CURRENT_DIR, "../data/dockerfile_tests/test_fail_command")
        # 测试是否抛出ParsingException
        with self.assertRaises(ParsingException):
            parse_shell_script_file_to_instruct_feature(input_script_path)
        print("test passed!")

    def test_parse_shell_script5(self):
        input_script_path = os.path.join(CURRENT_DIR, "../data/dockerfile_tests/test_end_of_CTLENDQUOTEMARK")
        print(parse_shell_script_file_to_instruct_feature(input_script_path))
