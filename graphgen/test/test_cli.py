import argparse
import builtins
import sys
import unittest
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
        sub_module = ['dependency', 'meta', 'ast', 'extractor']
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
            'ERROR: ./data/dependency/instruct_except_Dockerfile fails to be handled or the Dockerfile is incorrect!',
            file=sys.stderr)

    @patch('sys.argv', new=['test_cli.py', 'dependency', '-f', './data/dependency/Dockerfile1'])
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

    @patch('sys.argv', new=['test_cli.py', 'meta', '-f', './data/meta/abnormal_Dockerfile'])
    def test_input_abnormal_dockerfile(self):
        main()

    @patch('sys.argv', new=['test_cli.py', 'meta', '-f', './data/meta/instruct_except_Dockerfile'])
    @patch('builtins.print')
    def test_input_instruct_except_dockerfile(self, mock_print):
        main()
        mock_print.assert_any_call('ERROR: found invalid directive from！', file=sys.stderr)
        mock_print.assert_any_call(
            'ERROR: ./data/meta/instruct_except_Dockerfile fails to be handled or the Dockerfile is incorrect!',
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

    @patch('sys.argv', new=['test_cli.py', 'meta', '-d', './data/meta', '-o', './data/output/meta'])
    def test_abnormal_d_and_o_option2(self):
        main()


class TestASTModule(unittest.TestCase):
    @patch('sys.argv', new=['test_cli.py', 'ast', '-h'])
    def test_ast_module_help(self):
        module = 'ast'
        print(f"============================{module}=============================")
        with self.assertRaises(SystemExit):
            main()

    @patch('sys.argv', new=['test_cli.py', 'ast'])
    def test_error_situation(self):
        with self.assertRaises(ParameterMissError):
            main()

    @patch('sys.argv', new=['test_cli.py', 'ast', '-f', './data/ast/empty.sh'])
    @patch('builtins.print')
    def test_input_empty_file(self, mock_print):
        main()
        mock_print.assert_called_with("ERROR: ./data/ast/empty.sh does not contain valid shell commands!",
                                      file=sys.stderr)

    @patch('sys.argv', new=['test_cli.py', 'ast', '-f', './data/ast/abnormal_script.sh'])
    @patch('builtins.print')
    def test_input_abnormal_script_file(self, mock_print):
        main()
        mock_print.assert_called_with(f'ParsingException: shell script parse error!', file=sys.stderr)

    @patch('sys.argv', new=['test_cli.py', 'ast', '-f', './data/ast/grade.sh'])
    def test_input_normal_script_file(self):
        main()

    @patch('sys.argv', new=['test_cli.py', 'ast', '-f', './data/ast/run.sh'])
    def test_input_dockerfile_run(self):
        main()

    @patch('sys.argv',
           new=['test_cli.py', 'ast', '-f', './data/ast/grade.sh', '-o', './data/output/ast/grade_AST.json'])
    def test_f_and_o_option_together(self):
        main()

    @patch('sys.argv', new=['test_cli.py', 'ast', '-f', './data/ast/grade.sh', '--raw'])
    def test_raw_option_to_output(self):
        main()

    @patch('sys.argv', new=['test_cli.py', 'ast', '-f', './data/ast/grade.sh', '--detach'])
    def test_detach_option_to_output(self):
        main()

    @patch('sys.argv',
           new=['test_cli.py', 'ast', '-f', './data/ast/grade.sh', '--raw', '-o', './data/output/ast/grade_raw.txt'])
    def test_raw_option_to_file(self):
        main()

    @patch('sys.argv', new=['test_cli.py', 'ast', '-d', './data/ast'])
    def test_d_option_to_output(self):
        main()

    @patch('sys.argv', new=['test_cli.py', 'ast', '-d', './data/ast', '-o', './data/output/ast'])
    def test_d_and_o_option_to_output(self):
        main()

    @patch('sys.argv', new=['test_cli.py', 'ast', '-d', './data/ast', '-o', './data/output/ast', '--detach'])
    def test_d_and_o_and_detach_option_to_output(self):
        main()

    @patch('sys.argv', new=['test_cli.py', 'ast', '-d', './data/ast', '--raw'])
    def test_d_and_raw_option_to_output(self):
        main()

    @patch('sys.argv', new=['test_cli.py', 'ast', '-d', './data/ast', '-o', './data/output/ast/grade_raw.txt'])
    def test_abnormal_d_and_o_option(self):
        main()

    @patch('sys.argv', new=['test_cli.py', 'ast', '-d', './data/ast', '-o', './data/output/ast/a.txt'])
    def test_abnormal_d_and_o_option2(self):
        main()


class TestExtractorModule(unittest.TestCase):
    @patch('sys.argv', new=['test_cli.py', 'extractor', '-h'])
    def test_extractor_module_help(self):
        module = 'extractor'
        print(f"============================{module}=============================")
        with self.assertRaises(SystemExit):
            main()

    @patch('sys.argv', new=['test_cli.py', 'extractor'])
    def test_error_situation(self):
        with self.assertRaises(ParameterMissError):
            main()

    @patch('sys.argv', new=['test_cli.py', 'extractor', '-f', './data/extractor/empty.sh'])
    @patch('builtins.print')
    def test_input_empty_file(self, mock_print):
        main()
        mock_print.assert_called_with("ERROR: ./data/extractor/empty.sh does not contain valid shell commands!",
                                      file=sys.stderr)

    @patch('sys.argv', new=['test_cli.py', 'extractor', '-f', './data/extractor/example.sh'])
    def test_input_normal_script_file(self):
        main()

    @patch('sys.argv', new=['test_cli.py', 'extractor', '-f', './data/extractor/example.sh', '--only-parse'])
    def test_input_script_file_only_parse_option(self):
        main()

    @patch('sys.argv', new=['test_cli.py', 'extractor', '-f', './data/extractor/dependency_test.sh', '--detach'])
    def test_detach_option_to_output(self):
        main()

    @patch('sys.argv', new=['test_cli.py', 'extractor', '-f', './data/extractor/abnormal_script.sh'])
    @patch('builtins.print')
    def test_input_abnormal_script_file(self, mock_print):
        main()
        mock_print.assert_called_with(f'ParsingException: shell script parse error!', file=sys.stderr)

    @patch('sys.argv',
           new=['test_cli.py', 'extractor', '-f', './data/extractor/grade.sh', '-o',
                './data/output/extractor/grade_Feature.json'])
    def test_f_and_o_option_together(self):
        main()

    @patch('sys.argv', new=['test_cli.py', 'extractor', '-d', './data/extractor'])
    def test_d_option_to_output(self):
        main()

    @patch('sys.argv', new=['test_cli.py', 'extractor', '-d', './data/extractor', '--only-parse'])
    def test_d_and_only_parse_option_to_output(self):
        main()

    @patch('sys.argv', new=['test_cli.py', 'extractor', '-d', './data/extractor', '-o', './data/output/extractor'])
    def test_d_and_o_option_to_output(self):
        main()

    @patch('sys.argv',
           new=['test_cli.py', 'extractor', '-d', './data/extractor', '-o', './data/output/extractor', '--detach'])
    def test_d_and_o_and_detach_option_to_output(self):
        main()

    @patch('sys.argv',
           new=['test_cli.py', 'extractor', '-d', './data/extractor', '-o', './data/output/extractor/grade_raw.txt'])
    def test_abnormal_d_and_o_option(self):
        main()

    # @patch('sys.argv', new=['test_cli.py', 'extractor', '-d', './data/extractor', '-o', './data/output/aaa'])
    # def test_abnormal_d_and_o_option2(self):
    #     main()
