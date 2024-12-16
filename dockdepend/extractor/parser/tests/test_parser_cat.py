import unittest

from dockdepend.extractor.util_flag_option import make_arg_simple
from dockdepend.extractor.datatypes.BasicDatatypes import Operand
from dockdepend.extractor.datatypes.CommandInvocationInitial import CommandInvocationInitial
from dockdepend.extractor.parser.parser import parse


class TestParseCat(unittest.TestCase):
    def test_cat_1(self):
        parser_result = parse("cat -b -e in1.txt in2.txt")

        args = [make_arg_simple(["-b"]),
                make_arg_simple(["-e"])]
        operands = [Operand("in1.txt"),
                    Operand("in2.txt")]
        expected_result = CommandInvocationInitial("cat", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_cat_2(self):
        # this tests whether multiple flags with one - will be separated
        parser_result = parse("cat -be  in1.txt in2.txt")

        args = [make_arg_simple(["-b"]), make_arg_simple(["-e"])]
        operands = [Operand("in1.txt"),
                    Operand("in2.txt")]
        expected_result = CommandInvocationInitial("cat", args, operands)

        self.assertEqual(expected_result, parser_result)
