import unittest

from dockdepend.extractor.util_flag_option import make_arg_simple
from dockdepend.extractor.datatypes.BasicDatatypes import Operand
from dockdepend.extractor.datatypes.CommandInvocationInitial import CommandInvocationInitial
from dockdepend.extractor.parser.parser import parse


class TestParseSed(unittest.TestCase):
    def test_sed_1(self):
        parser_result = parse(
            "sed -i -e 's/MinSpareServers.*/MinSpareServers 1/g' /etc/apache2/mods-enabled/mpm_prefork.conf")

        args = [make_arg_simple(["-i"]),
                make_arg_simple(["-e", "s/MinSpareServers.*/MinSpareServers 1/g"])]
        operands = [Operand("/etc/apache2/mods-enabled/mpm_prefork.conf")]
        expected_result = CommandInvocationInitial("sed", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_sed_2(self):
        parser_result = parse("sed -f script.sed input.txt")

        args = [make_arg_simple(["-f", "script.sed"])]
        operands = [Operand("input.txt")]
        expected_result = CommandInvocationInitial("sed", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_sed_3(self):
        parser_result = parse("sed -e '/root/h' -e '$G' test")

        args = [make_arg_simple(["-e", "/root/h"]),
                make_arg_simple(["-e", "$G"])]
        operands = [Operand("test")]
        expected_result = CommandInvocationInitial("sed", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_sed_4(self):
        parser_result = parse("sed -i '/^#.* fr_FR.UTF-8.* /s/^#//' /etc/locale.gen")

        args = [make_arg_simple(["-i"])]
        operands = [Operand("/^#.* fr_FR.UTF-8.* /s/^#//"),
                    Operand("/etc/locale.gen")]
        expected_result = CommandInvocationInitial("sed", args, operands)

        self.assertEqual(expected_result, parser_result)
