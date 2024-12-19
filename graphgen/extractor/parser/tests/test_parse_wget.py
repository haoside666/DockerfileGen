import unittest

from graphgen.extractor.util_flag_option import make_arg_simple
from graphgen.extractor.datatypes.BasicDatatypes import Operand
from graphgen.extractor.datatypes.CommandInvocationInitial import CommandInvocationInitial
from graphgen.extractor.parser.parser import parse


class TestParseWget(unittest.TestCase):
    def test_wget_1(self):
        parser_result = parse("wget https://github.com/Kitware/CMake/releases/download/v3.14.0/cmake-3.14.0.tar.gz")

        args = []
        operands = [Operand("https://github.com/Kitware/CMake/releases/download/v3.14.0/cmake-3.14.0.tar.gz")]
        expected_result = CommandInvocationInitial("wget", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_wget_2(self):
        parser_result = parse("wget http://severalnines.com/downloads/cmon/s9s-repo.repo -P /etc/yum.repos.d/")

        args = [make_arg_simple(["-P", "/etc/yum.repos.d/"])]
        operands = [Operand("http://severalnines.com/downloads/cmon/s9s-repo.repo")]
        expected_result = CommandInvocationInitial("wget", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_wget_3(self):
        parser_result = parse(
            "wget -qO client.zip https://static2.askmrrobot.com/wowsite/client/AskMrRobotClient-any-1201.zip")

        args = [make_arg_simple(["-q"]),
                make_arg_simple(["-O", "client.zip"])]
        operands = [Operand("https://static2.askmrrobot.com/wowsite/client/AskMrRobotClient-any-1201.zip")]
        expected_result = CommandInvocationInitial("wget", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_wget_4(self):
        parser_result = parse(
            "wget --no-cache -O libnode.so.72 https://cdn.altv.mp/node-module/beta/x64_linux/libnode.so.72")

        args = [make_arg_simple(["--no-cache"]),
                make_arg_simple(["-O", "libnode.so.72"])]
        operands = [Operand("https://cdn.altv.mp/node-module/beta/x64_linux/libnode.so.72")]
        expected_result = CommandInvocationInitial("wget", args, operands)

        self.assertEqual(expected_result, parser_result)
