import unittest

from dockdepend.extractor.util_flag_option import make_arg_simple
from dockdepend.extractor.datatypes.BasicDatatypes import Operand
from dockdepend.extractor.datatypes.CommandInvocationInitial import CommandInvocationInitial
from dockdepend.extractor.parser.parser import parse


class TestParseUnzip(unittest.TestCase):
    def test_unzip_1(self):
        parser_result = parse("unzip /tmp/assp.mod.zip")

        args = []
        operands = [Operand("/tmp/assp.mod.zip")]
        expected_result = CommandInvocationInitial("unzip", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_unzip_2(self):
        parser_result = parse("unzip -d /bin /tmp/vault.zip")

        args = [make_arg_simple(["-d", "/bin"])]
        operands = [Operand("/tmp/vault.zip")]
        expected_result = CommandInvocationInitial("unzip", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_unzip_3(self):
        parser_result = parse("unzip -o ghost.zip -d /var/www/ghost")

        args = [make_arg_simple(["-o"]),
                make_arg_simple(["-d", "/var/www/ghost"])]
        operands = [Operand("ghost.zip")]
        expected_result = CommandInvocationInitial("unzip", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_unzip_4(self):
        parser_result = parse("unzip -q -j -u -o proj-datumgrid-latest.zip  -d /build_projgrids/share/proj")

        args = [make_arg_simple(["-q"]),
                make_arg_simple(["-j"]),
                make_arg_simple(["-u"]),
                make_arg_simple(["-o"]),
                make_arg_simple(["-d", "/build_projgrids/share/proj"])]
        operands = [Operand("proj-datumgrid-latest.zip")]
        expected_result = CommandInvocationInitial("unzip", args, operands)

        self.assertEqual(expected_result, parser_result)
