import unittest

from dockdepend.extractor.util_flag_option import make_arg_simple
from dockdepend.extractor.datatypes.BasicDatatypes import Operand
from dockdepend.extractor.datatypes.CommandInvocationInitial import CommandInvocationInitial
from dockdepend.extractor.parser.parser import parse


class TestParseLn(unittest.TestCase):
    def test_ln_1(self):
        parser_result = parse("ln node_modules/messer/index.js /usr/local/bin/messer")

        args = []
        operands = [Operand("node_modules/messer/index.js"),
                    Operand("/usr/local/bin/messer")]
        expected_result = CommandInvocationInitial("ln", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_ln_2(self):
        parser_result = parse("ln -sf /dev/stdout /var/log/netdata/collector.log")

        args = [make_arg_simple(["-s"]),
                make_arg_simple(["-f"])]
        operands = [Operand("/dev/stdout"),
                    Operand("/var/log/netdata/collector.log")]
        expected_result = CommandInvocationInitial("ln", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_ln_3(self):
        parser_result = parse("ln --symbolic /home/gradle/.gradle /root/.gradle")

        args = [make_arg_simple(["-s"])]
        operands = [Operand("/home/gradle/.gradle"),
                    Operand("/root/.gradle")]
        expected_result = CommandInvocationInitial("ln", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_ln_4(self):
        parser_result = parse("ln -t /usr/local/ /usr/bin/unrar")

        args = [make_arg_simple(["-t", "/usr/local/"])]
        operands = [Operand("/usr/bin/unrar")]
        expected_result = CommandInvocationInitial("ln", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_ln_5(self):
        parser_result = parse("ln -snf /usr/share/zoneinfo/$TZ/etc/localtime")

        args = [make_arg_simple(["-s"]),
                make_arg_simple(["-n"]),
                make_arg_simple(["-f"])]
        operands = [Operand("/usr/share/zoneinfo/$TZ/etc/localtime")]
        expected_result = CommandInvocationInitial("ln", args, operands)

        self.assertEqual(expected_result, parser_result)
