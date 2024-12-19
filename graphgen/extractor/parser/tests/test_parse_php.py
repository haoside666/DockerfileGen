import unittest

from graphgen.extractor.util_flag_option import make_arg_simple
from graphgen.extractor.datatypes.BasicDatatypes import Operand
from graphgen.extractor.datatypes.CommandInvocationInitial import CommandInvocationInitial
from graphgen.extractor.parser.parser import parse


class TestParsePhp(unittest.TestCase):
    def test_php_1(self):
        parser_result = parse("php composer.phar global require aws/aws-sdk-php")

        args = []
        operands = [Operand("composer.phar"),
                    Operand("global"),
                    Operand("require"),
                    Operand("aws/aws-sdk-php")]
        expected_result = CommandInvocationInitial("php", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_php_2(self):
        parser_result = parse("php composer.phar install")

        args = []
        operands = [Operand("composer.phar"),
                    Operand("install")]
        expected_result = CommandInvocationInitial("php", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_php_3(self):
        parser_result = parse("php composer-setup.php --install-dir=/usr/local/sbin --filename=composer")

        args = []
        operands = [Operand("composer-setup.php"),
                    Operand("--install-dir=/usr/local/sbin"),
                    Operand("--filename=composer")]
        expected_result = CommandInvocationInitial("php", args, operands)

        self.assertEqual(expected_result, parser_result)

    def test_php_4(self):
        parser_result = parse("php -r 'echo PHP_MAJOR_VERSION;'")

        args = [make_arg_simple(["-r", "echo PHP_MAJOR_VERSION;"])]
        operands = []
        expected_result = CommandInvocationInitial("php", args, operands)

        self.assertEqual(expected_result, parser_result)
