import unittest

from dockdepend.extractor.util_flag_option import make_arg_simple
from dockdepend.extractor.datatypes.BasicDatatypes import Operand
from dockdepend.extractor.datatypes.CommandInvocationInitial import CommandInvocationInitial
from dockdepend.extractor.parser.parser import parse


class TestParseCurl(unittest.TestCase):
    def test_curl_1(self):
        parser_result = parse(r"curl -o - https://raw.githubusercontent.com/creationix/nvm/1.0/install.sh")

        args = [make_arg_simple(["-o", "-"])]
        operands = [Operand("https://raw.githubusercontent.com/creationix/nvm/1.0/install.sh")]
        expected_result = CommandInvocationInitial("curl", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_curl_2(self):
        parser_result = parse(
            r"curl https://raw.githubusercontent.com/shamaazi/circle-lock-test/master/do-exclusively -o /usr/bin/do-exclusively")

        args = [make_arg_simple(["-o", "/usr/bin/do-exclusively"])]
        operands = [Operand("https://raw.githubusercontent.com/shamaazi/circle-lock-test/master/do-exclusively")]
        expected_result = CommandInvocationInitial("curl", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_curl_3(self):
        parser_result = parse(r"curl -L https://www.npmjs.com/install.sh")

        args = [make_arg_simple(["-L"])]
        operands = [Operand("https://www.npmjs.com/install.sh")]
        expected_result = CommandInvocationInitial("curl", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_curl_4(self):
        parser_result = parse(r"curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs")

        args = [make_arg_simple(["--proto", "=https"]),
                make_arg_simple(["--tlsv1.2"]),
                make_arg_simple(["-s"]),
                make_arg_simple(["-S"]),
                make_arg_simple(["-f"])]
        operands = [Operand("https://sh.rustup.rs")]
        expected_result = CommandInvocationInitial("curl", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_curl_5(self):
        parser_result = parse(
            r"curl --silent --show-error --location --fail --retry 3 --output /tmp/apache-maven.tar.gz https://www.apache.org/dist/maven/maven-3/3.6.0/binaries/apache-maven-3.6.0-bin.tar.gz")

        args = [make_arg_simple(["-s"]),
                make_arg_simple(["-S"]),
                make_arg_simple(["-L"]),
                make_arg_simple(["-f"]),
                make_arg_simple(["--retry", "3"]),
                make_arg_simple(["-o", "/tmp/apache-maven.tar.gz"])]
        operands = [Operand("https://www.apache.org/dist/maven/maven-3/3.6.0/binaries/apache-maven-3.6.0-bin.tar.gz")]
        expected_result = CommandInvocationInitial("curl", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_curl_6(self):
        parser_result = parse(r"curl -# -kLJOSsf https://sh.rustup.rs")

        args = [make_arg_simple(["-#"]),
                make_arg_simple(["-k"]),
                make_arg_simple(["-L"]),
                make_arg_simple(["-J"]),
                make_arg_simple(["-O"]),
                make_arg_simple(["-S"]),
                make_arg_simple(["-s"]),
                make_arg_simple(["-f"])]
        operands = [Operand("https://sh.rustup.rs")]
        expected_result = CommandInvocationInitial("curl", args, operands)

        self.assertEqual(expected_result, parser_result)
