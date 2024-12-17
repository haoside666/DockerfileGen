import sys

from dockdepend.shell_parse.datatypes.PrimitiveFeatureList import PrimitiveFeatureList
from dockdepend.shell_parse.libdash import parser
from dockdepend.shell_parse.shasta.json_to_ast import to_ast_node
from dockdepend.shell_parse.shasta.ast_node import AstNode
from typing import List, Tuple, Optional
from dockdepend.shell_parse.datatypes.CommandFeature import CommandFeature, read_jsons, union_command_feature, \
    get_command_feature_by_union_command_feature_list
from dockdepend.shell_parse.datatypes.InsturctFeatureInit import InstructFeatureInit
from dockdepend.config.definitions import TEMP_CMD_PATH, TEMP_VAR_C_LIST_PATH, TEMP_B_TYPE_PATH
from dockdepend.exception.CustomizedException import ExceptEndQuotemark, ParsingException
import re

Flag: bool = True


def clear_file(file_path):
    with open(file_path, 'w') as file:
        file.truncate(0)


# def get_raw_asts(input_script_path):
#     try:
#         global Flag
#         new_ast_objects = parser.parse(input_script_path, Flag)
#         if Flag:
#             Flag = False
#         untyped_ast_objects = []
#         for untyped_ast, original_text, linno_before, linno_after, in new_ast_objects:
#             untyped_ast_objects.append(untyped_ast)
#         return untyped_ast_objects
#     except Exception as e:
#         raise ParsingException('Exception: The shell parsing process fail')
#
#
# def parse_shell_to_asts(input_script_path) -> List[AstNode]:
#     try:
#         global Flag
#         new_ast_objects = parser.parse(input_script_path, Flag)
#         if Flag:
#             Flag = False
#         ## Transform the untyped ast objects to typed ones
#         typed_ast_objects = []
#         for untyped_ast, original_text, linno_before, linno_after, in new_ast_objects:
#             # print(untyped_ast)
#             typed_ast = to_ast_node(untyped_ast)
#             # print(typed_ast)
#             # typed_ast_objects.append((typed_ast, original_text, linno_before, linno_after))
#             typed_ast_objects.append(typed_ast)
#
#         return typed_ast_objects
#     except ParsingException as e:
#         # print(original_text)
#         print("The shell parsing process fails!")
#         raise
#
#
# def parse_shell_to_feature(input_script_path):
#     clear_file(TEMP_VAR_C_LIST_PATH)
#     clear_file(TEMP_B_TYPE_PATH)
#
#     try:
#         global Flag
#         new_ast_objects = parser.parse(input_script_path, Flag)
#         if Flag:
#             Flag = False
#         for untyped_ast, original_text, linno_before, linno_after, in new_ast_objects:
#             typed_ast = to_ast_node(untyped_ast)
#             feat: CommandFeature = typed_ast.feature()
#             print(feat)
#
#         print("-------------------------------")
#         print("--------------TEMP_VAR_C_LIST_PATH-----------------")
#         with open(TEMP_VAR_C_LIST_PATH, "r") as file:
#             print(file.read())
#         print("--------------TEMP_B_TYPE_PATH-----------------")
#         with open(TEMP_B_TYPE_PATH, "r") as file:
#             print(file.read())
#     except ParsingException as e:
#         # print(original_text)
#         # print(e)
#         # print("The shell parsing process fails!")
#         raise
#     except ExceptEndQuotemark as e:
#         print(f"error: {e.args[0]}!")
#         pass
#     except Exception as e:
#         raise
#
#
# def parse_shell_cmd_to_instruct_feature(cmd: str) -> Optional[InstructFeatureInit]:
#     with open(TEMP_CMD_PATH, "w") as file:
#         file.write(cmd)
#     clear_file(TEMP_VAR_C_LIST_PATH)
#     clear_file(TEMP_B_TYPE_PATH)
#     try:
#         global Flag
#         new_ast_objects = parser.parse(TEMP_CMD_PATH, Flag)
#         if Flag:
#             Flag = False
#         feat_list = []
#         for untyped_ast, _, _, _ in new_ast_objects:
#             typed_ast = to_ast_node(untyped_ast)
#             feat_list.append(typed_ast.feature())
#         assert len(feat_list) <= 1
#         if len(feat_list) == 0:
#             return None
#         var_c_list: List[str] = get_var_c_list()
#         b_type_feat: CommandFeature = get_b_type_feature()
#         total_cmd_feat: CommandFeature = union_command_feature(feat_list[0], b_type_feat)
#
#         return total_cmd_feat.get_instruct_feature_init_add_var_c_list(var_c_list)
#     except ParsingException:
#         print(f"ParsingException: The shell parsing process fails for the command: {cmd}", file=sys.stderr)
#         raise
#     except ExceptEndQuotemark as e:
#         cmd = process_inside_braces(cmd)
#         try:
#             return parse_shell_cmd_to_instruct_feature(cmd)
#         except Exception:
#             print(f"ExceptEndQuotemark: The shell parsing process fails for the command: {cmd}", file=sys.stderr)
#             raise
#     except Exception:
#         print(f"Exception: The shell parsing process fails for the command: {cmd}", file=sys.stderr)
#         raise


# 不考虑包括以下几种含有shell语法Dockerfile
# 含有复杂结构 即 含有def,for,while,if,case都为复杂命令
# 含有子命令，即``或$()形式
def parse_shell_cmd_to_primitive_feature(cmd: str) -> Optional[PrimitiveFeatureList]:
    with open(TEMP_CMD_PATH, "w") as file:
        file.write(cmd)
    clear_file(TEMP_VAR_C_LIST_PATH)
    clear_file(TEMP_B_TYPE_PATH)
    try:
        global Flag
        new_ast_objects = parser.parse(TEMP_CMD_PATH, Flag)
        if Flag:
            Flag = False
        feat_list = []
        for untyped_ast, _, _, _ in new_ast_objects:
            typed_ast = to_ast_node(untyped_ast)
            feat_list.append(typed_ast.feature())
        assert len(feat_list) <= 1
        if len(feat_list) == 0:
            return None
        var_c_list: List[str] = get_var_c_list()
        total_cmd_feat: PrimitiveFeatureList = feat_list[0]
        # 含有复杂结构
        if total_cmd_feat.is_complex:
            return None
        total_cmd_feat.add_var_c_list(list(set(var_c_list)))
        return total_cmd_feat
    except ParsingException:
        print(f"ParsingException: The shell parsing process fails for the command: {cmd}", file=sys.stderr)
        raise
    except ExceptEndQuotemark as e:
        cmd = process_inside_braces(cmd)
        try:
            return parse_shell_cmd_to_primitive_feature(cmd)
        except Exception:
            print(f"ExceptEndQuotemark: The shell parsing process fails for the command: {cmd}", file=sys.stderr)
            raise
    except Exception:
        print(f"Exception: The shell parsing process fails for the command: {cmd}", file=sys.stderr)
        raise


# def parse_shell_script_file_to_instruct_feature(input_script_path: str) -> Optional[InstructFeatureInit]:
#     clear_file(TEMP_VAR_C_LIST_PATH)
#     clear_file(TEMP_B_TYPE_PATH)
#     try:
#         global Flag
#         new_ast_objects = parser.parse(input_script_path, Flag)
#         if Flag:
#             Flag = False
#         feat_list = []
#         for untyped_ast, _, _, _ in new_ast_objects:
#             typed_ast = to_ast_node(untyped_ast)
#             feat_list.append(typed_ast.feature())
#         if len(feat_list) == 0:
#             return None
#
#         command_list_feature = get_command_feature_by_union_command_feature_list(feat_list)
#         var_c_list: List[str] = get_var_c_list()
#         b_type_feat: CommandFeature = get_b_type_feature()
#         total_cmd_feat: CommandFeature = union_command_feature(command_list_feature, b_type_feat)
#
#         return total_cmd_feat.get_instruct_feature_init_add_var_c_list(var_c_list)
#     except ParsingException:
#         print(f"ParsingException: The script file parse fail: {input_script_path}", file=sys.stderr)
#         raise
#     except ExceptEndQuotemark as e:
#         with open(input_script_path, 'r') as file, open(TEMP_CMD_PATH, "w") as tmp_file:
#             tmp_file.write(process_inside_braces(file.read()))
#         try:
#             return parse_shell_script_file_to_instruct_feature(TEMP_CMD_PATH)
#         except Exception:
#             print(f"ExceptEndQuotemark: The script file parse fail: {input_script_path}", file=sys.stderr)
#             raise
#     except Exception:
#         print(f"ParsingException: The script file parse fail: {input_script_path}", file=sys.stderr)
#         raise
#
#
# def parse_file_all_command_to_instruct_feature(input_script_path: str) -> List[Tuple[str, InstructFeatureInit]]:
#     try:
#         global Flag
#         new_ast_objects = parser.parse(input_script_path, Flag)
#         if Flag:
#             Flag = False
#
#         instruct_feat_init_list = []
#
#         for untyped_ast, _, _, _ in new_ast_objects:
#             # 清空临时文件
#             clear_file(TEMP_VAR_C_LIST_PATH)
#             clear_file(TEMP_B_TYPE_PATH)
#             typed_ast = to_ast_node(untyped_ast)
#             cmd_feat = typed_ast.feature()
#             var_c_list: List[str] = get_var_c_list()
#             b_type_feat: CommandFeature = get_b_type_feature()
#             total_cmd_feat: CommandFeature = union_command_feature(cmd_feat, b_type_feat)
#             instruct_feat_init = total_cmd_feat.get_instruct_feature_init_add_var_c_list(var_c_list)
#             instruct_feat_init_list.append((typed_ast.pretty(), instruct_feat_init))
#         return instruct_feat_init_list
#     except ParsingException:
#         print(f"ParsingException: The script file parse fail: {input_script_path}", file=sys.stderr)
#         raise
#     except ExceptEndQuotemark as e:
#         with open(input_script_path, 'r') as file, open(TEMP_CMD_PATH, "w") as tmp_file:
#             tmp_file.write(process_inside_braces(file.read()))
#         try:
#             return parse_file_all_command_to_instruct_feature(TEMP_CMD_PATH)
#         except Exception:
#             print(f"ExceptEndQuotemark: The script file parse fail: {input_script_path}", file=sys.stderr)
#             raise
#     except Exception:
#         print(f"ParsingException: The script file parse fail: {input_script_path}", file=sys.stderr)
#         raise


def get_var_c_list() -> List[str]:
    with open(TEMP_VAR_C_LIST_PATH, "r") as file:
        return [line.strip() for line in file]


def get_b_type_feature() -> CommandFeature:
    return read_jsons(TEMP_B_TYPE_PATH)


def process_inside_braces(cmd):
    # Match the contents of ${} with a regular expression
    pattern = r'\${([^}]*)}'

    matches = re.findall(pattern, cmd)

    for match in matches:
        if re.search(r"[^a-zA-Z0-9_]", match):
            filtered_string = re.sub(r'[^a-zA-Z0-9_]', '', match)
            cmd = cmd.replace(f'${{{match}}}', '${' + filtered_string + '}')

    return cmd
