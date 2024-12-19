import unittest

from graphgen.extractor.util_flag_option import make_arg_simple
from graphgen.extractor.datatypes.BasicDatatypes import Operand
from graphgen.extractor.datatypes.CommandInvocationInitial import CommandInvocationInitial
from graphgen.extractor.parser.parser import parse


class TestParseMkdir(unittest.TestCase):
    def test_mkdir_1(self):
        parser_result = parse("mkdir /app/data")

        args = []
        operands = [Operand("/app/data")]
        expected_result = CommandInvocationInitial("mkdir", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_mkdir_2(self):
        parser_result = parse("mkdir -p /jellyfin /media /cache")

        args = [make_arg_simple(["-p"])]
        operands = [Operand("/jellyfin"),
                    Operand("/media"),
                    Operand("/cache")]
        expected_result = CommandInvocationInitial("mkdir", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_mkdir_3(self):
        parser_result = parse("mkdir -m 775 -p /config/config.d 	/data/film 	/data/games 	/data/music")

        args = [make_arg_simple(["-m", "775"]),
                make_arg_simple(["-p"])]
        operands = [Operand("/config/config.d"),
                    Operand("/data/film"),
                    Operand("/data/games"),
                    Operand("/data/music")]
        expected_result = CommandInvocationInitial("mkdir", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_mkdir_4(self):
        parser_result = parse("mkdir -pv /root/lib/locale")

        args = [make_arg_simple(["-p"]),
                make_arg_simple(["-v"])]
        operands = [Operand("/root/lib/locale")]
        expected_result = CommandInvocationInitial("mkdir", args, operands)

        self.assertEqual(expected_result, parser_result)
