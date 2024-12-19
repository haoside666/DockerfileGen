import unittest

from graphgen.extractor.util_flag_option import make_arg_simple
from graphgen.extractor.datatypes.BasicDatatypes import Operand
from graphgen.extractor.datatypes.CommandInvocationInitial import CommandInvocationInitial
from graphgen.extractor.parser.parser import parse


class TestParseApt(unittest.TestCase):
    def test_apt_1(self):
        parser_result = parse("apt install mariadb-server mariadb-client -y")

        args = [make_arg_simple(["-y"])]
        operands = [Operand("install"),
                    Operand("mariadb-server"),
                    Operand("mariadb-client")]
        expected_result = CommandInvocationInitial("apt", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_apt_2(self):
        parser_result = parse("apt source -y -q nginx")

        args = [make_arg_simple(["-y"]),
                make_arg_simple(["-q"])]
        operands = [Operand("source"),
                    Operand("nginx")]
        expected_result = CommandInvocationInitial("apt", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_apt_3(self):
        parser_result = parse("apt upgrade -y")

        args = [make_arg_simple(["-y"])]
        operands = [Operand("upgrade")]
        expected_result = CommandInvocationInitial("apt", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_apt_4(self):
        parser_result = parse("apt install -y --allow-unauthenticated deb.torproject.org-keyring nodejs tor git tzdata")

        args = [make_arg_simple(["-y"]),
                make_arg_simple(["--allow-unauthenticated"])]
        operands = [Operand("install"),
                    Operand("deb.torproject.org-keyring"),
                    Operand("nodejs"),
                    Operand("tor"),
                    Operand("git"),
                    Operand("tzdata")]
        expected_result = CommandInvocationInitial("apt", args, operands)

        self.assertEqual(expected_result, parser_result)
