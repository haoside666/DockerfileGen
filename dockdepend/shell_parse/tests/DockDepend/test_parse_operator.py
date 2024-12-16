import unittest

from dockdepend.shell_parse.parse import parse_shell_to_asts
import os

CURRENT_DIR = os.path.dirname(__file__)


# Test: The shell operator resolves to an AST structure
class TestASTOperatorParse(unittest.TestCase):
    def test_parse_ascii(self):
        input_script_path = os.path.join(CURRENT_DIR, "../data/dockerfile_tests/ascii.txt")
        for typed_ast_object in parse_shell_to_asts(input_script_path):
            print(typed_ast_object)

    def test_parse_operator1_10(self):
        input_script_path = os.path.join(CURRENT_DIR, "../data/dockerfile_tests/operator1_10")
        for typed_ast_object in parse_shell_to_asts(input_script_path):
            print(typed_ast_object)

    def test_parse_operator11_20(self):
        input_script_path = os.path.join(CURRENT_DIR, "../data/dockerfile_tests/operator11-20")
        for typed_ast_object in parse_shell_to_asts(input_script_path):
            print(typed_ast_object)

    def test_parse_operator21_26(self):
        input_script_path = os.path.join(CURRENT_DIR, "../data/dockerfile_tests/operator21-26")
        for typed_ast_object in parse_shell_to_asts(input_script_path):
            print(typed_ast_object)
