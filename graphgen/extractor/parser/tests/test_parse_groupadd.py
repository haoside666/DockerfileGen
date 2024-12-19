import unittest

from graphgen.extractor.util_flag_option import make_arg_simple
from graphgen.extractor.datatypes.BasicDatatypes import Operand
from graphgen.extractor.datatypes.CommandInvocationInitial import CommandInvocationInitial
from graphgen.extractor.parser.parser import parse


class TestParseGroupadd(unittest.TestCase):
    def test_groupadd_1(self):
        parser_result = parse("groupadd -g 1004 jenkins")

        args = [make_arg_simple(["-g", "1004"])]
        operands = [Operand("jenkins")]
        expected_result = CommandInvocationInitial("groupadd", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_groupadd_2(self):
        parser_result = parse("groupadd -r activemq -g 433")

        args = [make_arg_simple(["-r"]),
                make_arg_simple(["-g", "433"])]
        operands = [Operand("activemq")]
        expected_result = CommandInvocationInitial("groupadd", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_groupadd_3(self):
        parser_result = parse("groupadd mysql")

        args = []
        operands = [Operand("mysql")]
        expected_result = CommandInvocationInitial("groupadd", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_groupadd_4(self):
        parser_result = parse("groupadd -f conan-2000 -g 2000")

        args = [make_arg_simple(["-f"]),
                make_arg_simple(["-g", "2000"])]
        operands = [Operand("conan-2000")]
        expected_result = CommandInvocationInitial("groupadd", args, operands)

        self.assertEqual(expected_result, parser_result)
