import unittest

from graphgen.extractor.datatypes.BasicDatatypes import Operand
from graphgen.extractor.datatypes.CommandInvocationInitial import CommandInvocationInitial
from graphgen.extractor.parser.parser import parse


class TestParseCd(unittest.TestCase):
    def test_cd_1(self):
        parser_result = parse("cd ../pythologist")

        args = []
        operands = [Operand("../pythologist")]
        expected_result = CommandInvocationInitial("cd", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_cd_2(self):
        parser_result = parse("cd ~")

        args = []
        operands = [Operand("~")]
        expected_result = CommandInvocationInitial("cd", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_cd_3(self):
        parser_result = parse("cd ~/rgtdata")

        args = []
        operands = [Operand("~/rgtdata")]
        expected_result = CommandInvocationInitial("cd", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_cd_4(self):
        parser_result = parse("cd filebeat*")

        args = []
        operands = [Operand("filebeat*")]
        expected_result = CommandInvocationInitial("cd", args, operands)

        self.assertEqual(expected_result, parser_result)
