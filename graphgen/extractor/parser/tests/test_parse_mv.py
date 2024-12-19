import unittest

from graphgen.extractor.util_flag_option import make_arg_simple
from graphgen.extractor.datatypes.BasicDatatypes import Operand
from graphgen.extractor.datatypes.CommandInvocationInitial import CommandInvocationInitial
from graphgen.extractor.parser.parser import parse


class TestParseMv(unittest.TestCase):
    def test_mv_1(self):
        parser_result = parse("mv *.pl bin/.")

        args = []
        operands = [Operand("*.pl"),
                    Operand("bin/.")]
        expected_result = CommandInvocationInitial("mv", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_mv_2(self):
        parser_result = parse("mv go /usr/bin/go")

        args = []
        operands = [Operand("go"),
                    Operand("/usr/bin/go")]
        expected_result = CommandInvocationInitial("mv", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_mv_3(self):
        parser_result = parse("mv frp_0.31.2_linux_amd64/frps frp_0.31.2_linux_amd64/frps.ini -t /usr/bin/frps")

        args = [make_arg_simple(["-t", "/usr/bin/frps"])]
        operands = [Operand("frp_0.31.2_linux_amd64/frps"),
                    Operand("frp_0.31.2_linux_amd64/frps.ini")]
        expected_result = CommandInvocationInitial("mv", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_mv_4(self):
        parser_result = parse(
            "mv -t /usr/bin/frps /frp_0.31.2_linux_amd64/frps /usr/bin/frps /frp_0.31.2_linux_amd64/frps.ini")

        args = [make_arg_simple(["-t", "/usr/bin/frps"])]
        operands = [Operand("/frp_0.31.2_linux_amd64/frps"),
                    Operand("/usr/bin/frps"),
                    Operand("/frp_0.31.2_linux_amd64/frps.ini")]
        expected_result = CommandInvocationInitial("mv", args, operands)

        self.assertEqual(expected_result, parser_result)
