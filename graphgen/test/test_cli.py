import argparse
import builtins
import os
import sys
import unittest
from functools import wraps
from unittest.mock import patch
from graphgen.cli import main
from graphgen.exception.CustomizedException import ParameterMissError, ParsingException


class TestMain(unittest.TestCase):
    @patch('sys.argv', new=['test_cli.py', '-h'])
    def test_main_help(self):
        # 测试main函数是否正确处理-h或--help参数
        # 注意: _HelpAction 默认会执行以下两个函数
        # parser.print_help()
        # parser.exit()
        with self.assertRaises(SystemExit):
            main()

    def test_all_sub_module_help(self):
        sub_module = ['dependency', 'meta', 'graph']
        for module in sub_module:
            print(f"============================{module}=============================")
            with patch('sys.argv', ['test_cli.py', module, '-h']):
                with self.assertRaises(SystemExit):
                    main()


class TestDependencyModule(unittest.TestCase):
    @patch('sys.argv', new=['test_cli.py', 'dependency', '-h'])
    def test_dependency_module_help(self):
        module = 'dependency'
        print(f"============================{module}=============================")
        with self.assertRaises(SystemExit):
            main()

    @patch('sys.argv', new=['test_cli.py', 'dependency'])
    def test_error_situation(self):
        with self.assertRaises(ParameterMissError):
            main()

    @patch('sys.argv', new=['test_cli.py', 'dependency', '-f', './data/dependency/Dockerfile_empty'])
    @patch('builtins.print')
    def test_input_empty_dockerfile(self, mock_print):
        main()
        mock_print.assert_called_with("ERROR: file with no instructions!", file=sys.stderr)

    @patch('sys.argv', new=['test_cli.py', 'dependency', '-f', './data/dependency/no_from_Dockerfile'])
    @patch('builtins.print')
    def test_input_no_from_dockerfile(self, mock_print):
        main()
        mock_print.assert_called_with(
            f"ERROR: Didn't parse to any valid build stage, make sure to include the FROM directive!", file=sys.stderr)

    @patch('sys.argv', new=['test_cli.py', 'dependency', '-f', './data/dependency/abnormal_Dockerfile'])
    def test_input_abnormal_dockerfile(self):
        main()

    @patch('sys.argv', new=['test_cli.py', 'dependency', '-f', './data/dependency/instruct_except_Dockerfile'])
    @patch('builtins.print')
    def test_input_instruct_except_dockerfile(self, mock_print):
        main()
        mock_print.assert_any_call('ERROR: found invalid directive from！', file=sys.stderr)
        mock_print.assert_any_call(
            'ERROR: dockerfile parse is abnormal,because found invalid directive from!',
            file=sys.stderr)

    @patch('sys.argv', new=['test_cli.py', 'dependency', '-f', './data/meta/Dockerfile_test_tool_package'])
    def test_input_normal_dockerfile(self):
        main()

    @patch('sys.argv', new=['test_cli.py', 'dependency', '-f', './data/dependency/Dockerfile5'])
    def test_input_normal_mutil_stage_dockerfile(self):
        main()

    @patch('sys.argv',
           new=['test_cli.py', 'dependency', '-f', './data/dependency/Dockerfile2', '--show-consistency-dependency'])
    def test_show_consistency_dependency_option(self):
        main()

    @patch('sys.argv', new=['test_cli.py', 'dependency', '-f', './data/dependency/Dockerfile2', '--ignore-side-effect'])
    def test_ignore_side_effect_option(self):
        main()

    @patch('sys.argv',
           new=['test_cli.py', 'dependency', '-f', './data/dependency/Dockerfile2', '--ignore-unknown-command'])
    def test_ignore_unknown_command_option(self):
        main()

    @patch('sys.argv', new=['test_cli.py', 'dependency', '-f', './data/dependency/Dockerfile1', '--simple-mode'])
    def test_simple_mode_option(self):
        main()

    @patch('sys.argv', new=['test_cli.py', 'dependency', '-f', './data/dependency/Dockerfile1', '--no-instruct-mode'])
    def test_no_instruct_mode_option(self):
        main()

    @patch('sys.argv', new=['test_cli.py', 'dependency', '-f', './data/dependency/Dockerfile1', '--build-info'])
    def test_build_info_option(self):
        main()

    @patch('sys.argv', new=['test_cli.py', 'dependency', '-d', './data/dependency', '-o', './data/output/dependency'])
    def test_d_and_o_option_to_output(self):
        main()


class TestMetaModule(unittest.TestCase):
    @patch('sys.argv', new=['test_cli.py', 'meta', '-h'])
    def test_meta_module_help(self):
        module = 'meta'
        print(f"============================{module}=============================")
        with self.assertRaises(SystemExit):
            main()

    @patch('sys.argv', new=['test_cli.py', 'meta'])
    def test_error_situation(self):
        with self.assertRaises(ParameterMissError):
            main()

    @patch('sys.argv', new=['test_cli.py', 'meta', '-f', './data/meta/Dockerfile_empty'])
    @patch('builtins.print')
    def test_input_empty_dockerfile(self, mock_print):
        main()
        mock_print.assert_called_with("ERROR: file with no instructions!", file=sys.stderr)

    @patch('sys.argv', new=['test_cli.py', 'meta', '-f', './data/meta/no_from_Dockerfile'])
    @patch('builtins.print')
    def test_input_no_from_dockerfile(self, mock_print):
        main()
        mock_print.assert_called_with(
            f"ERROR: Didn't parse to any valid build stage, make sure to include the FROM directive!", file=sys.stderr)

    @patch('sys.argv', new=['test_cli.py', 'meta', '-f', './data/meta/Dockerfile_test_tool_package'])
    def test_input_abnormal_dockerfile(self):
        main()

    @patch('sys.argv', new=['test_cli.py', 'meta', '-f', './data/meta/instruct_except_Dockerfile'])
    @patch('builtins.print')
    def test_input_instruct_except_dockerfile(self, mock_print):
        main()
        mock_print.assert_any_call('ERROR: found invalid directive from！', file=sys.stderr)
        mock_print.assert_any_call(
            'ERROR: dockerfile parse is abnormal,because found invalid directive from!',
            file=sys.stderr)

    @patch('sys.argv', new=['test_cli.py', 'meta', '-f', './data/meta/Dockerfile_all_instruction'])
    def test_input_normal_dockerfile(self):
        main()

    @patch('sys.argv', new=['test_cli.py', 'meta', '-f', './data/meta/Dockerfile_mutil'])
    def test_input_normal_mutil_stage_dockerfile(self):
        main()

    @patch('sys.argv',
           new=['test_cli.py', 'meta', '-f', './data/meta/Dockerfile_run_dependency_test', '-o',
                './data/output/meta/Dockerfile_run_dependency_test_meta.json'])
    def test_f_and_o_option_together(self):
        main()

    @patch('sys.argv',
           new=['test_cli.py', 'meta', '-f', './data/meta/Dockerfile_mutil', '-o',
                './data/output/meta/Dockerfile_mutil_meta.json'])
    def test_f_and_o_option_mutil_stage_dockerfile(self):
        main()

    @patch('sys.argv', new=['test_cli.py', 'meta', '-d', './data/meta'])
    def test_d_option_to_output(self):
        main()

    @patch('sys.argv', new=['test_cli.py', 'meta', '-d', './data/meta', '-o', './data/output/meta'])
    def test_d_and_o_option_to_output(self):
        main()

    @patch('sys.argv', new=['test_cli.py', 'meta', '-d', './data/meta', '-o', './data/output/meta/grade_raw.txt'])
    def test_abnormal_d_and_o_option(self):
        main()


class TestGraphModule(unittest.TestCase):
    @patch('sys.argv', new=['test_cli.py', 'graph', '-h'])
    def test_meta_module_help(self):
        module = 'graph'
        print(f"============================{module}=============================")
        with self.assertRaises(SystemExit):
            main()

    @patch('sys.argv', new=['test_cli.py', 'graph'])
    def test_error_situation(self):
        with self.assertRaises(ParameterMissError):
            main()

    @patch('sys.argv', new=['test_cli.py', 'graph', '-f', './data/meta/Dockerfile_empty'])
    @patch('builtins.print')
    def test_input_empty_dockerfile(self, mock_print):
        main()
        mock_print.assert_called_with("ERROR: file with no instructions!", file=sys.stderr)

    @patch('sys.argv', new=['test_cli.py', 'graph', '-f', './data/meta/no_from_Dockerfile'])
    @patch('builtins.print')
    def test_input_no_from_dockerfile(self, mock_print):
        main()
        mock_print.assert_called_with(
            f"ERROR: Didn't parse to any valid build stage, make sure to include the FROM directive!", file=sys.stderr)

    @patch('sys.argv', new=['test_cli.py', 'graph', '-f', './data/meta/instruct_except_Dockerfile'])
    @patch('builtins.print')
    def test_input_instruct_except_dockerfile(self, mock_print):
        main()
        mock_print.assert_any_call('ERROR: found invalid directive from！', file=sys.stderr)
        mock_print.assert_any_call(
            'ERROR: dockerfile parse is abnormal,because found invalid directive from!',
            file=sys.stderr)

    @patch('sys.argv', new=['test_cli.py', 'graph', '-f', './data/graph/Dockerfile_all_instruction'])
    def test_input_normal_dockerfile(self):
        main()

    @patch('sys.argv', new=['test_cli.py', 'graph', '-f', './data/graph/Dockerfile_mutil'])
    def test_input_normal_mutil_stage_dockerfile(self):
        main()

    @patch('sys.argv',
           new=['test_cli.py', 'graph', '-f', './data/graph/Dockerfile_test', '-o',
                './data/output/graph/Dockerfile_test_script.cypher'])
    def test_f_and_o_option_together(self):
        main()

    @patch('sys.argv',
           new=['test_cli.py', 'graph', '-f', './data/graph/Dockerfile_mutil', '-o',
                './data/output/graph/Dockerfile_mutil_script.cypher'])
    def test_f_and_o_option_mutil_stage_dockerfile(self):
        main()

    @patch('sys.argv', new=['test_cli.py', 'graph', '-d', './data/graph'])
    def test_d_option_to_output(self):
        main()

    # 请在此处修改文件名
    filename = "bartixxx32___hidden-eye###174526###4d82cb4515b4d36cb9080f7c76df076ca0580910_script.cypher"

    @patch('sys.argv',
           new=['test_cli.py', 'graph', '-f', f"/home/haoside/Desktop/input/{filename.replace('_script.cypher', '')}", '-o',
                f"/home/haoside/Desktop/output/{filename}"])
    def test_rebuild_single_script(self):
        main()

    @patch('sys.argv', new=['test_cli.py', 'graph',
                            '-f', '/home/haoside/Desktop/input/joselfonsecadt___nginx-php7.3###424887###87fc85f137178e83737843cc66c2660c1f3b20c9'])
    def test_input_abnormal_dockerfile(self):
        # /home/haoside/Desktop/input/usuresearch___scala-sbt-extras-gcloud###942632###a77df2cd8be3f9de87691ff7663ec67460bc19dc
        main()

    @patch('sys.argv', new=['test_cli.py', 'graph', '-d', '/home/haoside/Desktop/input', '-o', '/home/haoside/Desktop/output'])
    def test_d_and_o_option_to_output(self):
        main()

    @patch('sys.argv', new=['test_cli.py', 'graph', '-d', '/home/haoside/Desktop/input2'])
    def test_d_option(self):
        main()

    @patch('sys.argv', new=['test_cli.py', 'graph', '-d', './data/graph', '-o', './data/output/graph/grade_raw.txt'])
    @patch('builtins.print')
    def test_abnormal_d_and_o_option(self, mock_print):
        main()
        mock_print.assert_called_with(
            'ERROR: When using the -d option, the -o option must be a directory path!',
            file=sys.stderr)
