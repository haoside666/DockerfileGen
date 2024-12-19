import unittest

from graphgen.extractor.util_flag_option import make_arg_simple
from graphgen.extractor.datatypes.BasicDatatypes import Operand
from graphgen.extractor.datatypes.CommandInvocationInitial import CommandInvocationInitial
from graphgen.extractor.parser.parser import parse


class TestParseGit(unittest.TestCase):
    def test_git_1(self):
        parser_result = parse("git clone --depth 1 https://github.com/badili/odk_parser.git vendor")

        args = [make_arg_simple(["--depth", "1"])]
        operands = [Operand("clone"),
                    Operand("https://github.com/badili/odk_parser.git"),
                    Operand("vendor")]
        expected_result = CommandInvocationInitial("git", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_git_2(self):
        parser_result = parse(
            "git clone --single-branch --branch patch-1 https://github.com/grea09/phpipam-scripts.git")

        args = [make_arg_simple(["--single-branch"]),
                make_arg_simple(["-b", "patch-1"])]
        operands = [Operand("clone"),
                    Operand("https://github.com/grea09/phpipam-scripts.git")]
        expected_result = CommandInvocationInitial("git", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_git_3(self):
        parser_result = parse("git fetch -q --depth 1 origin main +refs/tags/*:refs/tags/*")

        args = [make_arg_simple(["-q"]),
                make_arg_simple(["--depth", "1"])]
        operands = [Operand("fetch"),
                    Operand("origin"),
                    Operand("main"),
                    Operand("+refs/tags/*:refs/tags/*")]
        expected_result = CommandInvocationInitial("git", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_git_4(self):
        parser_result = parse("git config --global --add safe.directory /app")

        args = [make_arg_simple(["--global"]),
                make_arg_simple(["--add"])]
        operands = [Operand("config"),
                    Operand("safe.directory"),
                    Operand("/app")]
        expected_result = CommandInvocationInitial("git", args, operands)

        self.assertEqual(expected_result, parser_result)
