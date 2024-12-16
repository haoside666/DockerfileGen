import unittest

from dockdepend.extractor.util_flag_option import make_arg_simple
from dockdepend.extractor.datatypes.BasicDatatypes import Operand
from dockdepend.extractor.datatypes.CommandInvocationInitial import CommandInvocationInitial
from dockdepend.extractor.parser.parser import parse


class TestParseNpm(unittest.TestCase):
    def test_npm_1(self):
        parser_result = parse("npm install -g cypress@11.0.1")

        args = [make_arg_simple(["-g"])]
        operands = [Operand("install"),
                    Operand("cypress@11.0.1")]
        expected_result = CommandInvocationInitial("npm", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_npm_2(self):
        parser_result = parse("npm install -g node-gyp")

        args = [make_arg_simple(["-g"])]
        operands = [Operand("install"),
                    Operand("node-gyp")]
        expected_result = CommandInvocationInitial("npm", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_npm_3(self):
        parser_result = parse("npm audit fix")

        args = []
        operands = [Operand("audit"),
                    Operand("fix")]
        expected_result = CommandInvocationInitial("npm", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_npm_4(self):
        parser_result = parse("npm test")

        args = []
        operands = [Operand("test")]
        expected_result = CommandInvocationInitial("npm", args, operands)

        self.assertEqual(expected_result, parser_result)
