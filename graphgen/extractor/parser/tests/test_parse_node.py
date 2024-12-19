import unittest

from graphgen.extractor.util_flag_option import make_arg_simple
from graphgen.extractor.datatypes.BasicDatatypes import Operand
from graphgen.extractor.datatypes.CommandInvocationInitial import CommandInvocationInitial
from graphgen.extractor.parser.parser import parse


class TestParseNode(unittest.TestCase):

    def test_node_1(self):
        parser_result = parse("node -v")

        args = [make_arg_simple(["-v"])]
        operands = []
        expected_result = CommandInvocationInitial("node", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_node_2(self):
        parser_result = parse("node install.js")

        args = []
        operands = [Operand("install.js")]
        expected_result = CommandInvocationInitial("node", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_node_3(self):
        parser_result = parse("node -p process.versions")

        args = [make_arg_simple(["-p", "process.versions"])]
        operands = []
        expected_result = CommandInvocationInitial("node", args, operands)

        self.assertEqual(expected_result, parser_result)
