import unittest

from graphgen.extractor.util_flag_option import make_arg_simple
from graphgen.extractor.datatypes.BasicDatatypes import Operand
from graphgen.extractor.datatypes.CommandInvocationInitial import CommandInvocationInitial
from graphgen.extractor.parser.parser import parse


class TestParseGem(unittest.TestCase):
    def test_gem_1(self):
        parser_result = parse("gem install mdl")

        args = []
        operands = [Operand("install"),
                    Operand("mdl")]
        expected_result = CommandInvocationInitial("gem", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_gem_2(self):
        parser_result = parse(
            "gem install --user-install --no-document --source ${CINC_GEM_SOURCE} --version ${INSPEC_VERSION} cinc-auditor-bin")

        args = [make_arg_simple(["--user-install"]),
                make_arg_simple(["-N"]),
                make_arg_simple(["-s", "${CINC_GEM_SOURCE}"]),
                make_arg_simple(["-v", "${INSPEC_VERSION}"])]
        operands = [Operand("install"),
                    Operand("cinc-auditor-bin")]
        expected_result = CommandInvocationInitial("gem", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_gem_3(self):
        parser_result = parse("gem install rexml -v 3.2.5")

        args = [make_arg_simple(["-v", "3.2.5"])]
        operands = [Operand("install"),
                    Operand("rexml")]
        expected_result = CommandInvocationInitial("gem", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_gem_4(self):
        parser_result = parse("gem update --system --no-document")

        args = [make_arg_simple(["--system"]),
                make_arg_simple(["-N"])]
        operands = [Operand("update")]
        expected_result = CommandInvocationInitial("gem", args, operands)

        self.assertEqual(expected_result, parser_result)
