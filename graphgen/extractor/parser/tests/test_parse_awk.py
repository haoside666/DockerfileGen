import unittest

from graphgen.extractor.util_flag_option import make_arg_simple
from graphgen.extractor.datatypes.BasicDatatypes import Operand
from graphgen.extractor.datatypes.CommandInvocationInitial import CommandInvocationInitial
from graphgen.extractor.parser.parser import parse


class TestParseAwk(unittest.TestCase):
    def test_awk_1(self):
        parser_result = parse("awk -F ':' '{print $0}' /etc/passwd")

        args = [make_arg_simple(["-F", ":"])]
        operands = [Operand("{print $0}"),
                    Operand("/etc/passwd")]
        expected_result = CommandInvocationInitial("awk", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_awk_2(self):
        # Reads from standard input
        parser_result = parse("awk -F '[ ,]' '{for(i=1;i<=NF;i++){print $i}}'")

        args = [make_arg_simple(["-F", "[ ,]"])]
        operands = [Operand("{for(i=1;i<=NF;i++){print $i}}")]
        expected_result = CommandInvocationInitial("awk", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_awk_3(self):
        # Reads from variable
        parser_result = parse("awk -v info='this is a test2010test1!' 'BEGIN{gsub(/[0-9]+/,\"!\",info);print info}' ")

        args = [make_arg_simple(["-v", "info=this is a test2010test1!"])]
        operands = [Operand("BEGIN{gsub(/[0-9]+/,\"!\",info);print info}")]
        expected_result = CommandInvocationInitial("awk", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_awk_4(self):
        parser_result = parse("awk 'FNR == NR { seen[$0] = 1; next } !seen[$0]' file1.txt file2.txt")

        args = []
        operands = [Operand("FNR == NR { seen[$0] = 1; next } !seen[$0]"),
                    Operand("file1.txt"),
                    Operand("file2.txt")]
        expected_result = CommandInvocationInitial("awk", args, operands)

        self.assertEqual(expected_result, parser_result)
