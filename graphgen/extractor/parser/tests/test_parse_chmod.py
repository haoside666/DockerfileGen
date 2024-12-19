import unittest

from graphgen.extractor.util_flag_option import make_arg_simple
from graphgen.extractor.datatypes.BasicDatatypes import Operand
from graphgen.extractor.datatypes.CommandInvocationInitial import CommandInvocationInitial
from graphgen.extractor.parser.parser import parse


class TestParseChmod(unittest.TestCase):
    def test_chmod_1(self):
        parser_result = parse("chmod g+rwx /var/run/nginx.pid")

        args = []
        operands = [Operand("g+rwx"),
                    Operand("/var/run/nginx.pid")]
        expected_result = CommandInvocationInitial("chmod", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_chmod_2(self):
        parser_result = parse("chmod 775 /run")

        args = []
        operands = [Operand("775"),
                    Operand("/run")]
        expected_result = CommandInvocationInitial("chmod", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_chmod_3(self):
        parser_result = parse(
            "chmod 755 /app/webscrapper.py /app/wind_tracker.py /app/telegram_bot.py /app/consts.py /app/windInfo.py")

        args = []
        operands = [Operand("755"),
                    Operand("/app/webscrapper.py"),
                    Operand("/app/wind_tracker.py"),
                    Operand("/app/telegram_bot.py"),
                    Operand("/app/consts.py"),
                    Operand("/app/windInfo.py")]
        expected_result = CommandInvocationInitial("chmod", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_chmod_4(self):
        parser_result = parse("chmod -R 4775 /qbittorrent /Downloads /Downloads/temp")

        args = [make_arg_simple(["-R"])]
        operands = [Operand("4775"),
                    Operand("/qbittorrent"),
                    Operand("/Downloads"),
                    Operand("/Downloads/temp")]
        expected_result = CommandInvocationInitial("chmod", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_chmod_5(self):
        parser_result = parse("chmod --reference file1.txt file2.txt")

        args = [make_arg_simple(["--reference", "file1.txt"])]
        operands = [Operand("file2.txt")]
        expected_result = CommandInvocationInitial("chmod", args, operands)

        self.assertEqual(expected_result, parser_result)
