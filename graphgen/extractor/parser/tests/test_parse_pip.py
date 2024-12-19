import unittest

from graphgen.extractor.util_flag_option import make_arg_simple
from graphgen.extractor.datatypes.BasicDatatypes import Operand
from graphgen.extractor.datatypes.CommandInvocationInitial import CommandInvocationInitial
from graphgen.extractor.parser.parser import parse


class TestParsePip(unittest.TestCase):
    def test_pip_1(self):
        parser_result = parse("pip install -e .")

        args = [make_arg_simple(["-e", "."])]
        operands = [Operand("install")]
        expected_result = CommandInvocationInitial("pip", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_pip_2(self):
        parser_result = parse("pip install /usr/src/mimic")

        args = []
        operands = [Operand("install"),
                    Operand("/usr/src/mimic")]
        expected_result = CommandInvocationInitial("pip", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_pip_3(self):
        parser_result = parse("pip3 install --no-cache-dir -r requirements.txt")

        args = [make_arg_simple(["--no-cache-dir"]),
                make_arg_simple(["-r", "requirements.txt"])]
        operands = [Operand("install")]
        expected_result = CommandInvocationInitial("pip3", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_pip_4(self):
        parser_result = parse("pip install .")

        args = []
        operands = [Operand("install"),
                    Operand(".")]
        expected_result = CommandInvocationInitial("pip", args, operands)

        self.assertEqual(expected_result, parser_result)
