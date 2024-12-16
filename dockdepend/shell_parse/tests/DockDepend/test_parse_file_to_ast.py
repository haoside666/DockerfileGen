import unittest

from dockdepend.shell_parse.parse import parse_shell_to_asts
import os

CURRENT_DIR = os.path.dirname(__file__)


# Test: Parse various shell script (file format) to AST format
class TestASTCmdFileParse(unittest.TestCase):
    # # Test standard inputs
    # def test_parse_stdin(self):
    #     input_script_path = "-"
    #     print(parse_shell_to_asts(input_script_path))

    def test_command_node_parse(self):
        input_script_path = os.path.join(CURRENT_DIR, "../data/dockerfile_tests/test_command_node")
        for typed_ast_object in parse_shell_to_asts(input_script_path):
            print(typed_ast_object)

    def test_pipe_node_parse(self):
        input_script_path = os.path.join(CURRENT_DIR, "../data/dockerfile_tests/test_pipe_node")
        for typed_ast_object in parse_shell_to_asts(input_script_path):
            print(typed_ast_object)

    def test_if_node_parse(self):
        input_script_path = os.path.join(CURRENT_DIR, "../data/dockerfile_tests/test_if_node")
        for typed_ast_object in parse_shell_to_asts(input_script_path):
            print(typed_ast_object)

    def test_while_node_parse(self):
        input_script_path = os.path.join(CURRENT_DIR, "../data/dockerfile_tests/test_while_node")
        for typed_ast_object in parse_shell_to_asts(input_script_path):
            print(typed_ast_object)

    def test_for_node_parse(self):
        input_script_path = os.path.join(CURRENT_DIR, "../data/dockerfile_tests/test_for_node")
        for typed_ast_object in parse_shell_to_asts(input_script_path):
            print(typed_ast_object)

    def test_fun_node_parse(self):
        input_script_path = os.path.join(CURRENT_DIR, "../data/dockerfile_tests/test_fun_node")
        for typed_ast_object in parse_shell_to_asts(input_script_path):
            print(typed_ast_object)

    def test_case_node_parse(self):
        input_script_path = os.path.join(CURRENT_DIR, "../data/dockerfile_tests/test_case_node")
        for typed_ast_object in parse_shell_to_asts(input_script_path):
            print(typed_ast_object)

    def test_Vtype_parse(self):
        input_script_path = os.path.join(CURRENT_DIR, "data/shell_tests/Vtype")
        for typed_ast_object in parse_shell_to_asts(input_script_path):
            print(typed_ast_object)
