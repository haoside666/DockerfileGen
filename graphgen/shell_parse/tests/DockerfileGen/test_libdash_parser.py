import unittest

from graphgen.config.definitions import TEMP_CMD_PATH
from graphgen.shell_parse.datatypes.PrimitiveFeatureList import PrimitiveFeatureList
from graphgen.shell_parse.libdash import parser
from graphgen.shell_parse.shasta.json_to_ast import to_ast_node

temp_cmd_path = TEMP_CMD_PATH


def test_parser(inputPath, flag):
    cmd = "curl -sSL https://github.com/sgerrand/alpine-pkg-glibc/releases/download/2.29-r0/glibc-2.29-r0.apk > /tmp/glibc.apk"
    with open(temp_cmd_path, "w") as file:
        file.write(cmd)
    new_ast_objects = parser.parse(inputPath, flag)
    feat_list = []
    for untyped_ast, _, _, _ in new_ast_objects:
        typed_ast = to_ast_node(untyped_ast)
        feat_list.append(typed_ast.feature())
    assert len(feat_list) <= 1
    if len(feat_list) == 0:
        return "None"
    total_cmd_feat: PrimitiveFeatureList = feat_list[0]
    print(total_cmd_feat)


class TestASTCmdParse(unittest.TestCase):
    def test_parser(self):
        cmd = "curl -sSL https://github.com/sgerrand/alpine-pkg-glibc/releases/download/2.29-r0/glibc-2.29-r0.apk > /tmp/glibc.apk"
        cmd2 = "apk add --no-cache /tmp/glibc.apk"
        cmd3 = "wget http://ftp.gnu.org/gnu/gawk/gawk-5.1.0.tar.xz"
        with open(temp_cmd_path, "w") as file:
            file.write(cmd)

        test_parser(temp_cmd_path, True)
        temp_cmd_path2 = temp_cmd_path + "2"
        with open(temp_cmd_path2 + "2", "w") as file:
            file.write(cmd2)
        test_parser(temp_cmd_path2, True)
        temp_cmd_path3 = temp_cmd_path + "3"
        with open(temp_cmd_path3, "w") as file:
            file.write(cmd3)
        test_parser(temp_cmd_path3, True)
