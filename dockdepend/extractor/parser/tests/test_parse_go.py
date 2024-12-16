import unittest

from dockdepend.extractor.util_flag_option import make_arg_simple
from dockdepend.extractor.datatypes.BasicDatatypes import Operand
from dockdepend.extractor.datatypes.CommandInvocationInitial import CommandInvocationInitial
from dockdepend.extractor.parser.parser import parse


class TestParseGo(unittest.TestCase):
    def test_go_1(self):
        parser_result = parse(
            "go build -o main -trimpath -ldflags \"-X main.version=$(command)\"")

        args = [make_arg_simple(["-o", "main"]),
                make_arg_simple(["-trimpath"]),
                make_arg_simple(["-ldflags", "-X main.version=$(command)"])]
        operands = [Operand("build")]
        expected_result = CommandInvocationInitial("go", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_go_2(self):
        parser_result = parse("go get -v -u -d honnef.co/go/tools/cmd/keyify")

        args = [make_arg_simple(["-v"]),
                make_arg_simple(["-u"]),
                make_arg_simple(["-d"])]
        operands = [Operand("get"),
                    Operand("honnef.co/go/tools/cmd/keyify")]
        expected_result = CommandInvocationInitial("go", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_go_3(self):
        parser_result = parse("go test -v models_test.go")

        args = [make_arg_simple(["-v"])]
        operands = [Operand("test"),
                    Operand("models_test.go")]
        expected_result = CommandInvocationInitial("go", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_go_4(self):
        parser_result = parse("go mod edit -require github.com/caddyserver/caddy@v${CADDY_VERSION}")

        args = [make_arg_simple(["-require", "github.com/caddyserver/caddy@v${CADDY_VERSION}"])]
        operands = [Operand("mod"),
                    Operand("edit")]
        expected_result = CommandInvocationInitial("go", args, operands)

        self.assertEqual(expected_result, parser_result)
