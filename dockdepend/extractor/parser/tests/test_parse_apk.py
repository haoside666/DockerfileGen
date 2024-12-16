import unittest

from dockdepend.extractor.util_flag_option import make_arg_simple
from dockdepend.extractor.datatypes.BasicDatatypes import Operand
from dockdepend.extractor.datatypes.CommandInvocationInitial import CommandInvocationInitial
from dockdepend.extractor.parser.parser import parse


class TestParseApk(unittest.TestCase):
    def test_apk_1(self):
        parser_result = parse("apk --repository https://repos.azul.com/zulu/alpine --no-cache add zulu13-jre")

        args = [make_arg_simple(["-X", "https://repos.azul.com/zulu/alpine"]),
                make_arg_simple(["--no-cache"])]
        operands = [Operand("add"),
                    Operand("zulu13-jre")]
        expected_result = CommandInvocationInitial("apk", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_apk_2(self):
        parser_result = parse("apk add --no-cache libcurl=7.61.1-r1 libffi-dev=3.2.1-r4 libffi=3.2.1-r4 npm=8.14.0-r0")

        args = [make_arg_simple(["--no-cache"])]
        operands = [Operand("add"),
                    Operand("libcurl=7.61.1-r1"),
                    Operand("libffi-dev=3.2.1-r4"),
                    Operand("libffi=3.2.1-r4"),
                    Operand("npm=8.14.0-r0")]
        expected_result = CommandInvocationInitial("apk", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_apk_3(self):
        parser_result = parse("apk del -X http://dl-cdn.alpinelinux.org/alpine/v3.6/main --no-cache cppunit-dev")

        args = [make_arg_simple(["-X", "http://dl-cdn.alpinelinux.org/alpine/v3.6/main"]),
                make_arg_simple(["--no-cache"])]
        operands = [Operand("del"),
                    Operand("cppunit-dev")]
        expected_result = CommandInvocationInitial("apk", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_apk_4(self):
        parser_result = parse("apk del build-base autoconf")

        args = []
        operands = [Operand("del"),
                    Operand("build-base"),
                    Operand("autoconf")]
        expected_result = CommandInvocationInitial("apk", args, operands)

        self.assertEqual(expected_result, parser_result)
