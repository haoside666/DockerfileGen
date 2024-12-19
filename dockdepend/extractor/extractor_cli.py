import os.path
import sys
from typing import List, Optional, Tuple, Union

# create parser
from dockdepend.extractor.feature_extract.feature_extract import get_feature_info_from_cmd_invocation_in_pipe_mode
from dockdepend.extractor.datatypes.CommandInvocationInitial import CommandInvocationInitial
from dockdepend.extractor.datatypes.CommandInvocationWithFeature import CommandInvocationWithFeature
from dockdepend.extractor.datatypes.CommandListFeature import CommandListFeature, make_command_list_feature
from dockdepend.extractor.datatypes.CommandInvocationFeature import CommandInvocationFeature, \
    union_xargs_command_feature, make_pipe_feature
from dockdepend.extractor.parser.parser import parse, parse_xargs
from dockdepend.extractor.datatypes.StringProcessor import StringProcessor


def get_cmd_inv_feature_in_pipe_mode(cmd_invocation: str, pipe: str = "") -> \
        Tuple[Optional[CommandInvocationFeature], str, str]:
    cmd_invocation = StringProcessor(cmd_invocation).process()
    if cmd_invocation.startswith("xargs"):
        return get_xargs_feature_in_pipe_mode(cmd_invocation, pipe)
    else:
        command_invocation: CommandInvocationInitial = parse(cmd_invocation)
        cmd_name = command_invocation.cmd_name
        if cmd_name == "cd":
            if len(command_invocation.operand_list) == 1:
                return None, command_invocation.operand_list[0].get_name(), pipe
            elif len(command_invocation.operand_list) == 0:
                return None, "~", pipe
            else:
                assert False
        else:
            cmd_inv_after_io, feature_info, pipe = get_feature_info_from_cmd_invocation_in_pipe_mode(command_invocation,
                                                                                                     pipe)
            if feature_info is not None:
                cmd_inv_with_feature: CommandInvocationWithFeature = feature_info.apply_feature_info_to_command_invocation(
                    cmd_inv_after_io)
                cmd_feat: CommandInvocationFeature = cmd_inv_with_feature.get_command_feature_info()
                cmd_feat.set_cmd_info(*command_invocation.get_info_list())
                return cmd_feat, "", pipe
            else:
                print(f"error: {cmd_invocation}", file=sys.stderr)
                raise


def get_cmd_inv_feature_in_cmd_mode(cmd_invocation: str) -> Tuple[Optional[CommandInvocationFeature], str]:
    return get_cmd_inv_feature_in_pipe_mode(cmd_invocation)[:2]


def get_command_list_feature(command_list: Union[List[str], List[List[str]]], attribute_user: str,
                             attribute_dir: str) -> Tuple[CommandListFeature, str]:
    cmd_inv_feat_list = []
    for command in command_list:
        if isinstance(command, str):
            cmd_feature, current_dir = get_cmd_inv_feature_in_cmd_mode(command)
            if cmd_feature is None:
                attribute_dir = get_real_attribute_dir(attribute_user, attribute_dir, current_dir)
                cmd_feature = CommandInvocationFeature("cd", [attribute_dir], [], [], [], [])
                cmd_feature.set_cmd_operand_list([attribute_dir])
                cmd_inv_feat_list.append(cmd_feature)
            else:
                cmd_feature.get_real_input_and_output_path_by_path_pointer(attribute_dir, attribute_user)
                cmd_inv_feat_list.append(cmd_feature)
        elif isinstance(command, List):
            pipe = ""
            pipe_feat_list = []
            for item in command:
                cmd_feature, current_dir, pipe = get_cmd_inv_feature_in_pipe_mode(item, pipe)
                if cmd_feature is None:
                    attribute_dir = get_real_attribute_dir(attribute_user, attribute_dir, current_dir)
                    cmd_feature = CommandInvocationFeature("cd", [attribute_dir], [], [], [], [])
                    cmd_feature.set_cmd_operand_list([attribute_dir])
                    pipe_feat_list.append(cmd_feature)
                else:
                    cmd_feature.get_real_input_and_output_path_by_path_pointer(attribute_dir, attribute_user)
                    pipe_feat_list.append(cmd_feature)
            feat = make_pipe_feature(pipe_feat_list)
            cmd_inv_feat_list.append(feat)

    instruct_feature: CommandListFeature = make_command_list_feature(cmd_inv_feat_list)
    return instruct_feature, attribute_dir


def get_command_feature_list(command_list: Union[List[str], List[List[str]]], attribute_user: str,
                             attribute_dir: str) -> Tuple[List[CommandInvocationFeature], str]:
    cmd_inv_feat_list = []
    for command in command_list:
        if isinstance(command, str):
            cmd_feature, current_dir = get_cmd_inv_feature_in_cmd_mode(command)
            if cmd_feature is None:
                attribute_dir = get_real_attribute_dir(attribute_user, attribute_dir, current_dir)
                cmd_feature = CommandInvocationFeature("cd", [attribute_dir], [], [], [], [])
                cmd_inv_feat_list.append(cmd_feature)
            else:
                cmd_feature.get_real_input_and_output_path_by_path_pointer(attribute_dir, attribute_user)
                cmd_inv_feat_list.append(cmd_feature)
        elif isinstance(command, List):
            pipe = ""
            for item in command:
                cmd_feature, current_dir, pipe = get_cmd_inv_feature_in_pipe_mode(item, pipe)
                if cmd_feature is None:
                    attribute_dir = get_real_attribute_dir(attribute_user, attribute_dir, current_dir)
                    cmd_feature = CommandInvocationFeature("cd", [attribute_dir], [], [], [], [])
                    cmd_inv_feat_list.append(cmd_feature)
                else:
                    cmd_feature.get_real_input_and_output_path_by_path_pointer(attribute_dir, attribute_user)
                    cmd_inv_feat_list.append(cmd_feature)

    return cmd_inv_feat_list, attribute_dir


def get_real_attribute_dir(attribute_user: str, attribute_dir: str, current_dir: str):
    if os.path.isabs(current_dir):
        attribute_dir = current_dir
    else:
        if "~" in current_dir:
            if attribute_user == "root":
                attribute_dir = current_dir.replace("~", "/root")
            else:
                attribute_dir = current_dir.replace("~", f"/home/{attribute_user}")
        else:
            attribute_dir = os.path.abspath(os.path.join(attribute_dir, current_dir))
    return attribute_dir


def get_xargs_feature_in_pipe_mode(cmd_invocation: str, pipe: str = "") -> Tuple[CommandInvocationFeature, str, str]:
    cmd_inv_init1, cmd_inv_init2 = parse_xargs(cmd_invocation)
    cmd_inv_after_io1, feature_info1, pipe = get_feature_info_from_cmd_invocation_in_pipe_mode(cmd_inv_init1, pipe)
    obj1: CommandInvocationFeature = feature_info1.apply_feature_info_to_command_invocation(
        cmd_inv_after_io1).get_command_feature_info()

    if cmd_inv_init2 is None:
        return obj1, "", pipe
    else:
        cmd_inv_after_io2, feature_info2, pipe = get_feature_info_from_cmd_invocation_in_pipe_mode(cmd_inv_init2,
                                                                                                   pipe)
        obj2: CommandInvocationFeature = feature_info2.apply_feature_info_to_command_invocation(
            cmd_inv_after_io2).get_command_feature_info()
        obj1.set_cmd_info(*cmd_inv_init1.get_info_list())
        obj2.set_cmd_info(*cmd_inv_init2.get_info_list())
        return union_xargs_command_feature(obj1, obj2), "", pipe


def get_command_list_parse_result(command_list: Union[List[str], List[List[str]]]):
    parse_result: List[
        Union[Tuple[str, CommandInvocationInitial], Tuple[List[str], List[CommandInvocationInitial]]]] = []
    for command in command_list:
        if isinstance(command, str):
            cmd_invocation = command
            cmd_invocation = StringProcessor(cmd_invocation).process()
            command_invocation: CommandInvocationInitial = parse(cmd_invocation)
            parse_result.append((cmd_invocation, command_invocation))
        elif isinstance(command, List):
            command_invocation: List[CommandInvocationInitial] = []
            for item in command:
                cmd_invocation = item
                cmd_invocation = StringProcessor(cmd_invocation).process()
                command_invocation.append(parse(cmd_invocation))

            parse_result.append((command, command_invocation))
    return parse_result
