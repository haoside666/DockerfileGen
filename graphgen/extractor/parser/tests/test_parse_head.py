import unittest

from graphgen.extractor.util_flag_option import make_arg_simple
from graphgen.extractor.datatypes.BasicDatatypes import Operand
from graphgen.extractor.datatypes.CommandInvocationInitial import CommandInvocationInitial
from graphgen.extractor.parser.parser import parse


class TestParseHead(unittest.TestCase):
    def test_head_1(self):
        parser_result = parse("head -n -2 /etc/bash.bashrc")

        args = [make_arg_simple(["-n", "-2"])]
        operands = [Operand("/etc/bash.bashrc")]
        expected_result = CommandInvocationInitial("head", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_head_2(self):
        parser_result = parse("head -c 5 /dev/random")

        args = [make_arg_simple(["-c", "5"])]
        operands = [Operand("/dev/random")]
        expected_result = CommandInvocationInitial("head", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_head_3(self):
        parser_result = parse("head /etc/passwd")

        args = []
        operands = [Operand("/etc/passwd")]
        expected_result = CommandInvocationInitial("head", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_head_4(self):
        parser_result = parse("head -n 5 /etc/passwd")

        args = [make_arg_simple(["-n", "5"])]
        operands = [Operand("/etc/passwd")]
        expected_result = CommandInvocationInitial("head", args, operands)

        self.assertEqual(expected_result, parser_result)
