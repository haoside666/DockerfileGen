import unittest

from graphgen.extractor.util_flag_option import make_arg_simple
from graphgen.extractor.datatypes.BasicDatatypes import Operand
from graphgen.extractor.datatypes.CommandInvocationInitial import CommandInvocationInitial
from graphgen.extractor.parser.parser import parse


class TestParseUseradd(unittest.TestCase):
    def test_useradd_1(self):
        parser_result = parse("useradd -ms /bin/bash emundo")

        args = [make_arg_simple(["-m"]),
                make_arg_simple(["-s", "/bin/bash"])]
        operands = [Operand("emundo")]
        expected_result = CommandInvocationInitial("useradd", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_useradd_2(self):
        parser_result = parse("useradd -c 'Emby' -d /usr/lib/emby-server -g emby -m -r emby")

        args = [make_arg_simple(["-c", "Emby"]),
                make_arg_simple(["-d", "/usr/lib/emby-server"]),
                make_arg_simple(["-g", "emby"]),
                make_arg_simple(["-m"]),
                make_arg_simple(["-r"])]
        operands = [Operand("emby")]
        expected_result = CommandInvocationInitial("useradd", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_useradd_3(self):
        parser_result = parse("useradd --create-home --home-dir $HOME user")

        args = [make_arg_simple(["-m"]),
                make_arg_simple(["-d", "$HOME"])]
        operands = [Operand("user")]
        expected_result = CommandInvocationInitial("useradd", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_useradd_4(self):
        parser_result = parse("useradd -u 1001 -G www-data -d /gtrader -s /bin/bash -M gtrader")

        args = [make_arg_simple(["-u", "1001"]),
                make_arg_simple(["-G", "www-data"]),
                make_arg_simple(["-d", "/gtrader"]),
                make_arg_simple(["-s", "/bin/bash"]),
                make_arg_simple(["-M"])]
        operands = [Operand("gtrader")]
        expected_result = CommandInvocationInitial("useradd", args, operands)

        self.assertEqual(expected_result, parser_result)

    # The old version of -h is equivalent to the current -d
    def test_useradd_5(self):
        parser_result = parse("useradd -h /home/tfansible -u 1000 -s /bin/bash tfansible -D")

        args = [make_arg_simple(["-h"]),
                make_arg_simple(["-u", "1000"]),
                make_arg_simple(["-s", "/bin/bash"]),
                make_arg_simple(["-D"])]
        operands = [Operand("/home/tfansible"), Operand("tfansible")]
        expected_result = CommandInvocationInitial("useradd", args, operands)

        self.assertEqual(expected_result, parser_result)
