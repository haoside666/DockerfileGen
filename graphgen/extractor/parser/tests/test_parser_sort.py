import unittest

from graphgen.extractor.util_flag_option import make_arg_simple
from graphgen.extractor.datatypes.BasicDatatypes import Operand
from graphgen.extractor.datatypes.CommandInvocationInitial import CommandInvocationInitial
from graphgen.extractor.parser.parser import parse


class TestParseSort(unittest.TestCase):
    def test_sort_1(self):
        parser_result = parse("sort in1.txt in2.txt")

        args = []
        operands = [Operand("in1.txt"),
                    Operand("in2.txt")]
        expected_result = CommandInvocationInitial("sort", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_sort_2(self):
        parser_result = parse("sort -b -o result.txt in1.txt in2.txt")

        args = [make_arg_simple(["-b"]), make_arg_simple(["-o", "result.txt"])]
        operands = [Operand("in1.txt"),
                    Operand("in2.txt")]
        expected_result = CommandInvocationInitial("sort", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_sort_3(self):
        # this tests whether options will be mapped to their primary representation
        parser_result = parse("sort -b --output result.txt in1.txt in2.txt")

        args = [make_arg_simple(["-b"]), make_arg_simple(["-o", "result.txt"])]
        operands = [Operand("in1.txt"),
                    Operand("in2.txt")]
        expected_result = CommandInvocationInitial("sort", args, operands)

        self.assertEqual(expected_result, parser_result)
