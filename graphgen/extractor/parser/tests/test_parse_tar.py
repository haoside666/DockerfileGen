import json
import unittest

from graphgen.extractor.util_flag_option import make_arg_simple
from graphgen.extractor.datatypes.BasicDatatypes import Operand
from graphgen.extractor.datatypes.CommandInvocationInitial import CommandInvocationInitial
from graphgen.extractor.parser.parser import parse


class TestParseTar(unittest.TestCase):
    def test_tar_1(self):
        parser_result = parse("tar -zxvf gromacs-2018.3.tar.gz")

        args = [make_arg_simple(["-z"]),
                make_arg_simple(["-x"]),
                make_arg_simple(["-v"]),
                make_arg_simple(["-f", "gromacs-2018.3.tar.gz"])]
        operands = []
        expected_result = CommandInvocationInitial("tar", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_tar_2(self):
        parser_result = parse("tar -zxC /usr/src -f ngx_devel_kit.tar.gz")

        args = [make_arg_simple(["-z"]),
                make_arg_simple(["-x"]),
                make_arg_simple(["-C", "/usr/src"]),
                make_arg_simple(["-f", "ngx_devel_kit.tar.gz"])]
        operands = []
        expected_result = CommandInvocationInitial("tar", args, operands)

        self.assertEqual(expected_result, parser_result)
        print(json.dumps(parser_result.to_dict(), indent=4))

    def test_tar_3(self):
        parser_result = parse("tar -cvf /tmp/lo.tar instdir/")

        args = [make_arg_simple(["-c"]),
                make_arg_simple(["-v"]),
                make_arg_simple(["-f", "/tmp/lo.tar"])]
        operands = [Operand("instdir/")]
        expected_result = CommandInvocationInitial("tar", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_tar_4(self):
        parser_result = parse("tar --strip-components 1 -xaf perl-5.8.9.tar.bz2 -C /usr/src/perl")

        args = [make_arg_simple(["--strip-components", "1"]),
                make_arg_simple(["-x"]),
                make_arg_simple(["-a"]),
                make_arg_simple(["-f", "perl-5.8.9.tar.bz2"]),
                make_arg_simple(["-C", "/usr/src/perl"])]
        operands = []
        expected_result = CommandInvocationInitial("tar", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_tar_5(self):
        parser_result = parse("tar -cvf myarchive.tar -C /mydata files")

        args = [make_arg_simple(["-c"]),
                make_arg_simple(["-v"]),
                make_arg_simple(["-f", "myarchive.tar"]),
                make_arg_simple(["-C", "/mydata"])]
        operands = [Operand("files")]
        expected_result = CommandInvocationInitial("tar", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_tar_6(self):
        parser_result = parse("tar -czvf archive.tar.gz file1.txt file2.txt directory1 directory2")

        args = [make_arg_simple(["-c"]),
                make_arg_simple(["-z"]),
                make_arg_simple(["-v"]),
                make_arg_simple(["-f", "archive.tar.gz"])]
        operands = [Operand("file1.txt"), Operand("file2.txt"), Operand("directory1"), Operand("directory2")]
        expected_result = CommandInvocationInitial("tar", args, operands)

        self.assertEqual(expected_result, parser_result)
        print(json.dumps(parser_result.to_dict(), indent=4))
