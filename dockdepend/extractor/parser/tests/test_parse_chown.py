import unittest

from dockdepend.extractor.util_flag_option import make_arg_simple
from dockdepend.extractor.datatypes.BasicDatatypes import Operand
from dockdepend.extractor.datatypes.CommandInvocationInitial import CommandInvocationInitial
from dockdepend.extractor.parser.parser import parse


class TestParseChown(unittest.TestCase):
    def test_chown_1(self):
        parser_result = parse("chown root nginx.conf")

        args = []
        operands = [Operand("root"),
                    Operand("nginx.conf")]
        expected_result = CommandInvocationInitial("chown", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_chown_2(self):
        parser_result = parse("chown www-data:www-data /bin/composer")

        args = []
        operands = [Operand("www-data:www-data"),
                    Operand("/bin/composer")]
        expected_result = CommandInvocationInitial("chown", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_chown_3(self):
        parser_result = parse("chown -R user:user /usr/src/rpd-purs")

        args = [make_arg_simple(["-R"])]
        operands = [Operand("user:user"),
                    Operand("/usr/src/rpd-purs")]
        expected_result = CommandInvocationInitial("chown", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_chown_4(self):
        parser_result = parse("chown -Rh logstash. /etc/logstash /opt/logstash")

        args = [make_arg_simple(["-R"]),
                make_arg_simple(["-h"])]
        operands = [Operand("logstash."),
                    Operand("/etc/logstash"),
                    Operand("/opt/logstash")]
        expected_result = CommandInvocationInitial("chown", args, operands)

        self.assertEqual(expected_result, parser_result)
