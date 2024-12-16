import unittest

from dockdepend.extractor.util_flag_option import make_arg_simple
from dockdepend.extractor.datatypes.BasicDatatypes import Operand
from dockdepend.extractor.datatypes.CommandInvocationInitial import CommandInvocationInitial
from dockdepend.extractor.parser.parser import parse


class TestParseGrep(unittest.TestCase):
    def test_grep_1(self):
        parser_result = parse(r"grep -e '^\s*def' -m 3 -n test.py")

        args = [make_arg_simple(["-e", r"^\s*def"]),
                make_arg_simple(["-m", "3"]),
                make_arg_simple(["-n"])]
        operands = [Operand("test.py")]
        expected_result = CommandInvocationInitial("grep", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_grep_2(self):
        parser_result = parse(r"grep -y 'hello' file.txt")

        args = [make_arg_simple(["-i"])]
        operands = [Operand("hello"), Operand("file.txt")]
        expected_result = CommandInvocationInitial("grep", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_grep_3(self):
        parser_result = parse(r"grep -f '1.txt' file.txt")

        args = [make_arg_simple(["-f", "1.txt"]), ]
        operands = [Operand("file.txt")]
        expected_result = CommandInvocationInitial("grep", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_grep_4(self):
        parser_result = parse(r"grep -f - a.txt")
        args = [make_arg_simple(["-f", "-"]), ]
        operands = [Operand("a.txt")]
        expected_result = CommandInvocationInitial("grep", args, operands)

        self.assertEqual(expected_result, parser_result)
