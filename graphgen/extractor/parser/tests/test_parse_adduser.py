import unittest

from graphgen.extractor.util_flag_option import make_arg_simple
from graphgen.extractor.datatypes.BasicDatatypes import Operand
from graphgen.extractor.datatypes.CommandInvocationInitial import CommandInvocationInitial
from graphgen.extractor.parser.parser import parse


class TestParseAdduser(unittest.TestCase):
    def test_adduser_1(self):
        parser_result = parse("adduser -u 82 -D -S -h /var/cache/nginx -G nginx nginx")

        args = [make_arg_simple(["-u", "82"]),
                make_arg_simple(["-D"]),
                make_arg_simple(["-S"]),
                make_arg_simple(["-h", "/var/cache/nginx"]),
                make_arg_simple(["-G", "nginx"])]
        operands = [Operand("nginx")]
        expected_result = CommandInvocationInitial("adduser", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_adduser_2(self):
        parser_result = parse("adduser -D -g \"\" -s /bin/sh -G go-dnsmasq go-dnsmasq")

        args = [make_arg_simple(["-D"]),
                make_arg_simple(["-g", ""]),
                make_arg_simple(["-s", "/bin/sh"]),
                make_arg_simple(["-G", "go-dnsmasq"])]
        operands = [Operand("go-dnsmasq")]
        expected_result = CommandInvocationInitial("adduser", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_adduser_3(self):
        parser_result = parse("adduser --disabled-password --gecos '' --ingroup app --home /app --uid 10001 app")

        args = [make_arg_simple(["--disabled-password"]),
                make_arg_simple(["--gecos", ""]),
                make_arg_simple(["--ingroup", "app"]),
                make_arg_simple(["--home", "/app"]),
                make_arg_simple(["-u", "10001"])]
        operands = [Operand("app")]
        expected_result = CommandInvocationInitial("adduser", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_adduser_4(self):
        parser_result = parse(
            "adduser -h /var/lib/transmission -D -u 502 -g transmission -G transmission -s /sbin/nologin transmission")

        args = [make_arg_simple(["-h", "/var/lib/transmission"]),
                make_arg_simple(["-D"]),
                make_arg_simple(["-u", "502"]),
                make_arg_simple(["-g", "transmission"]),
                make_arg_simple(["-G", "transmission"]),
                make_arg_simple(["-s", "/sbin/nologin"])]
        operands = [Operand("transmission")]
        expected_result = CommandInvocationInitial("adduser", args, operands)

        self.assertEqual(expected_result, parser_result)
