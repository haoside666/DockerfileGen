import unittest

from graphgen.extractor.util_flag_option import make_arg_simple
from graphgen.extractor.datatypes.BasicDatatypes import Operand
from graphgen.extractor.datatypes.CommandInvocationInitial import CommandInvocationInitial
from graphgen.extractor.parser.parser import parse_xargs


class TestParseXargs(unittest.TestCase):
    def test_xargs_1(self):
        parser_result1, parser_result2 = parse_xargs("xargs -a /tmp/apt-packages.txt apt-get install -y")

        args = [make_arg_simple(["-a", "/tmp/apt-packages.txt"])]
        operands = []
        expected_result1 = CommandInvocationInitial("xargs", args, operands)
        args = [make_arg_simple(["-y"])]
        operands = [Operand("install")]
        expected_result2 = CommandInvocationInitial("apt-get", args, operands)

        assert expected_result1 == parser_result1
        assert expected_result2 == parser_result2

    def test_xargs_2(self):
        parser_result1, parser_result2 = parse_xargs("xargs rm -rf /filelist")

        args = []
        operands = []
        expected_result1 = CommandInvocationInitial("xargs", args, operands)
        args = [make_arg_simple(["-r"]),
                make_arg_simple(["-f"])]
        operands = [Operand("/filelist")]
        expected_result2 = CommandInvocationInitial("rm", args, operands)

        assert expected_result1 == parser_result1
        assert expected_result2 == parser_result2

    def test_xargs_3(self):
        parser_result1, parser_result2 = parse_xargs("xargs -n 1 -L 1 pip3 install")

        args = [make_arg_simple(["-n", "1"]),
                make_arg_simple(["-L", "1"])]
        operands = []
        expected_result1 = CommandInvocationInitial("xargs", args, operands)
        args = []
        operands = [Operand("install")]
        expected_result2 = CommandInvocationInitial("pip3", args, operands)

        assert expected_result1 == parser_result1
        assert expected_result2 == parser_result2

    # curl -s https://api.github.com/repos/philippe44/AirConnect/releases/latest | grep tarball_url | cut -d '"' -f 4 | xargs curl -L -o airconnect.tar.gz
    def test_xargs_4(self):
        parser_result1, parser_result2 = parse_xargs("xargs curl -L -o airconnect.tar.gz")

        args = []
        operands = []
        expected_result1 = CommandInvocationInitial("xargs", args, operands)
        args = [make_arg_simple(["-L"]),
                make_arg_simple(["-o", "airconnect.tar.gz"])]
        operands = []
        expected_result2 = CommandInvocationInitial("curl", args, operands)

        assert expected_result1 == parser_result1
        assert expected_result2 == parser_result2
