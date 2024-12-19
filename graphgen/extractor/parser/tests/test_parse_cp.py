import unittest

from graphgen.extractor.util_flag_option import make_arg_simple
from graphgen.extractor.datatypes.BasicDatatypes import Operand
from graphgen.extractor.datatypes.CommandInvocationInitial import CommandInvocationInitial
from graphgen.extractor.parser.parser import parse


class TestParseCp(unittest.TestCase):
    def test_cp_1(self):
        parser_result = parse("cp -R -p /usr/local/nagios/etc /bk/nagios")

        args = [make_arg_simple(["-R"]),
                make_arg_simple(["-p"])]
        operands = [Operand("/usr/local/nagios/etc"),
                    Operand("/bk/nagios")]
        expected_result = CommandInvocationInitial("cp", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_cp_2(self):
        parser_result = parse("cp -rf /build/prom/include/* /build/promhttp/include/* /out/usr/include/")

        args = [make_arg_simple(["-r"]),
                make_arg_simple(["-f"])]
        operands = [Operand("/build/prom/include/*"),
                    Operand("/build/promhttp/include/*"),
                    Operand("/out/usr/include/")]
        expected_result = CommandInvocationInitial("cp", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_cp_3(self):
        parser_result = parse("cp /tmp/uci/*.so /tmp/dst/lib/")

        args = []
        operands = [Operand("/tmp/uci/*.so"),
                    Operand("/tmp/dst/lib/")]
        expected_result = CommandInvocationInitial("cp", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_cp_4(self):
        parser_result = parse("cp -t destination file1.txt file2.txt")

        args = [make_arg_simple(["-t", "destination"])]
        operands = [Operand("file1.txt"),
                    Operand("file2.txt")]
        expected_result = CommandInvocationInitial("cp", args, operands)

        self.assertEqual(expected_result, parser_result)
