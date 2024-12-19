import unittest

from graphgen.extractor.util_flag_option import make_arg_simple
from graphgen.extractor.datatypes.BasicDatatypes import Operand
from graphgen.extractor.datatypes.CommandInvocationInitial import CommandInvocationInitial
from graphgen.extractor.parser.parser import parse


class TestParseYum(unittest.TestCase):
    def test_yum_1(self):
        parser_result = parse("yum -q -y install zulu15-jre")

        args = [make_arg_simple(["-q"]),
                make_arg_simple(["-y"])]
        operands = [Operand("install"),
                    Operand("zulu15-jre")]
        expected_result = CommandInvocationInitial("yum", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_yum_2(self):
        parser_result = parse(
            "yum install -y -q https://s3.amazonaws.com/amazon-ssm-us-east-1/3.1.1374.0/linux_amd64/amazon-ssm-agent.rpm")

        args = [make_arg_simple(["-y"]),
                make_arg_simple(["-q"])]
        operands = [Operand("install"),
                    Operand(
                        "https://s3.amazonaws.com/amazon-ssm-us-east-1/3.1.1374.0/linux_amd64/amazon-ssm-agent.rpm")]
        expected_result = CommandInvocationInitial("yum", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_yum_3(self):
        parser_result = parse("yum clean all")

        args = []
        operands = [Operand("clean"),
                    Operand("all")]
        expected_result = CommandInvocationInitial("yum", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_yum_4(self):
        parser_result = parse("yum remove -y git glibc-devel.i686")

        args = [make_arg_simple(["-y"])]
        operands = [Operand("remove"),
                    Operand("git"),
                    Operand("glibc-devel.i686")]
        expected_result = CommandInvocationInitial("yum", args, operands)

        self.assertEqual(expected_result, parser_result)
