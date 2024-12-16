import unittest

from dockdepend.extractor.util_flag_option import make_arg_simple
from dockdepend.extractor.datatypes.BasicDatatypes import Operand
from dockdepend.extractor.datatypes.CommandInvocationInitial import CommandInvocationInitial
from dockdepend.extractor.parser.parser import parse


class TestParseRm(unittest.TestCase):
    def test_rm_1(self):
        parser_result = parse(r"rm -rf /var/lib/apt/lists/*")

        args = [make_arg_simple(["-r"]),
                make_arg_simple(["-f"])]
        operands = [Operand("/var/lib/apt/lists/*")]
        expected_result = CommandInvocationInitial("rm", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_rm_2(self):
        parser_result = parse(r"rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*")

        args = [make_arg_simple(["-r"]),
                make_arg_simple(["-f"])]
        operands = [Operand("/var/lib/apt/lists/*"), Operand("/tmp/*"), Operand("/var/tmp/*")]
        expected_result = CommandInvocationInitial("rm", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_rm_3(self):
        parser_result = parse(r"rm xcache.tar.gz")

        args = []
        operands = [Operand("xcache.tar.gz")]
        expected_result = CommandInvocationInitial("rm", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_rm_4(self):
        parser_result = parse(r"rm -rf dist /tmp/validator.zip")

        args = [make_arg_simple(["-r"]),
                make_arg_simple(["-f"])]
        operands = [Operand("dist"), Operand("/tmp/validator.zip")]
        expected_result = CommandInvocationInitial("rm", args, operands)

        self.assertEqual(expected_result, parser_result)
