import sys
from typing import Set, Literal, List, Dict, Tuple, Optional

import shlex
from graphgen.extractor.datatypes.BasicDatatypes import FlagOption, Flag, Option, Operand
from graphgen.extractor.datatypes.CommandInvocationInitial import CommandInvocationInitial
from graphgen.extractor.parser.util_parser import get_json_data
from graphgen.extractor.config.definitions import special_command_list_in_parse


def parse(command: str) -> CommandInvocationInitial:
    try:
        parsed_elements_list: List[str] = shlex.split(command)
    except ValueError:
        parsed_elements_list: List[str] = command.split()
    cmd_name: str = parsed_elements_list[0]
    try:
        if cmd_name in special_command_list_in_parse:
            return parse_special_command(parsed_elements_list)
        else:
            return parse_general_command(parsed_elements_list)
    except Exception:
        print(f"The feature extract process fails for the command: {command}", file=sys.stderr)
        flag_option_list, operand_list = default_process_when_default_json_is_used(parsed_elements_list)
        return CommandInvocationInitial(cmd_name, flag_option_list, operand_list)


# For the xargs command, this is equivalent to two commands
def parse_xargs(command: str) -> Tuple[CommandInvocationInitial, Optional[CommandInvocationInitial]]:
    parsed_elements_list: List[str] = shlex.split(command)
    cmd_name: str = parsed_elements_list[0]
    set_of_all_flags, dict_flag_to_primary_repr, set_of_all_options, dict_option_to_primary_repr, flags = \
        get_flag_and_option_basic_info(cmd_name)

    assert not flags
    flag_option_list: List[FlagOption] = []
    i = 1

    while i < len(parsed_elements_list):
        potential_flag_or_option = parsed_elements_list[i]
        if potential_flag_or_option in set_of_all_flags:
            add_flag_to_flag_option_list(dict_flag_to_primary_repr, potential_flag_or_option, flag_option_list)
        elif (potential_flag_or_option in set_of_all_options) and ((i + 1) < len(parsed_elements_list)):
            add_option_to_flag_option_list(dict_option_to_primary_repr, parsed_elements_list[i],
                                           parsed_elements_list[i + 1], flag_option_list)
            i += 1  # since we consumed another term for the argument
        elif all_is_individually_flags(potential_flag_or_option, set_of_all_flags):
            for split_el in list(potential_flag_or_option[1:]):
                flag: Flag = Flag(f'-{split_el}')
                flag_option_list.append(flag)
        else:
            break
        i += 1
    cmd_inv_init1: CommandInvocationInitial = CommandInvocationInitial(cmd_name, flag_option_list, [])
    # For xargs, next one is Operand, The follow-up is another command section
    another_cmd = " ".join(parsed_elements_list[i:])
    if another_cmd != "":
        cmd_inv_init2: CommandInvocationInitial = parse(another_cmd)
        return cmd_inv_init1, cmd_inv_init2
    else:
        return cmd_inv_init1, None


# For the general case where option can't be mixed with flag
def parse_general_command(parsed_elements_list: List[str]) -> CommandInvocationInitial:
    cmd_name: str = parsed_elements_list[0]
    set_of_all_flags, dict_flag_to_primary_repr, set_of_all_options, dict_option_to_primary_repr, flags = \
        get_flag_and_option_basic_info(cmd_name)

    if flags:
        flag_option_list, operand_list = default_process_when_default_json_is_used(parsed_elements_list)
        return CommandInvocationInitial(cmd_name, flag_option_list, operand_list)
    else:
        # parse list of command invocation terms
        flag_option_list: List[FlagOption] = []
        operand_list: List[Operand] = []
        i = 1

        while i < len(parsed_elements_list):
            potential_flag_or_option = parsed_elements_list[i]
            if potential_flag_or_option in set_of_all_flags:
                add_flag_to_flag_option_list(dict_flag_to_primary_repr, potential_flag_or_option, flag_option_list)
            elif (potential_flag_or_option in set_of_all_options) and ((i + 1) < len(parsed_elements_list)):
                add_option_to_flag_option_list(dict_option_to_primary_repr, parsed_elements_list[i],
                                               parsed_elements_list[i + 1], flag_option_list)
                i += 1  # since we consumed another term for the argument
            elif all_is_individually_flags(potential_flag_or_option, set_of_all_flags):
                for split_el in list(potential_flag_or_option[1:]):
                    flag: Flag = Flag(f'-{split_el}')
                    flag_option_list.append(flag)
            else:
                operand_list.append(Operand(potential_flag_or_option))
            i += 1

        return CommandInvocationInitial(cmd_name, flag_option_list, operand_list)


# For the special case where option can be mixed with flag
def parse_special_command(parsed_elements_list: List[str]) -> CommandInvocationInitial:
    cmd_name: str = parsed_elements_list[0]
    set_of_all_flags, dict_flag_to_primary_repr, set_of_all_options, dict_option_to_primary_repr, flags = \
        get_flag_and_option_basic_info(cmd_name)

    if flags:
        flag_option_list, operand_list = default_process_when_default_json_is_used(parsed_elements_list)
        return CommandInvocationInitial(cmd_name, flag_option_list, operand_list)
    else:
        # parse list of command invocation terms
        flag_option_list: List[FlagOption] = []
        operand_list: List[Operand] = []
        i = 1

        while i < len(parsed_elements_list):
            potential_flag_or_option = parsed_elements_list[i]
            if potential_flag_or_option in set_of_all_flags:
                add_flag_to_flag_option_list(dict_flag_to_primary_repr, potential_flag_or_option, flag_option_list)
            elif (potential_flag_or_option in set_of_all_options) and ((i + 1) < len(parsed_elements_list)):
                add_option_to_flag_option_list(dict_option_to_primary_repr, parsed_elements_list[i],
                                               parsed_elements_list[i + 1], flag_option_list)
                i += 1  # since we consumed another term for the argument
            elif all_but_last_is_individually_flags(potential_flag_or_option, set_of_all_flags, set_of_all_options):
                for split_el in list(potential_flag_or_option[1:-1]):
                    flag: Flag = Flag(f'-{split_el}')
                    flag_option_list.append(flag)

                split_el = f'-{potential_flag_or_option[-1]}'
                if split_el in set_of_all_flags:
                    flag: Flag = Flag(split_el)
                    flag_option_list.append(flag)
                else:
                    option_arg_as_string: str = parsed_elements_list[i + 1]
                    option = Option(split_el, option_arg_as_string)
                    flag_option_list.append(option)
                    i += 1
            else:
                operand_list.append(Operand(potential_flag_or_option))
            i += 1
        return CommandInvocationInitial(cmd_name, flag_option_list, operand_list)


def add_flag_to_flag_option_list(dict_flag_to_primary_repr: Dict, flag_str: str, flag_option_list: List):
    flag_name_as_string: str = dict_flag_to_primary_repr.get(flag_str, flag_str)
    flag: Flag = Flag(flag_name_as_string)
    flag_option_list.append(flag)


def add_option_to_flag_option_list(dict_option_to_primary_repr: Dict, option_name: str, option_arg: str,
                                   flag_option_list: List):
    option_name_as_string: str = dict_option_to_primary_repr.get(option_name, option_name)
    option = Option(option_name_as_string, option_arg)
    flag_option_list.append(option)


# Returns true if using the default json file
def get_flag_and_option_basic_info(cmd_name) -> (Set[str], Dict[str, str], Set[str], Dict[str, str], bool):
    json_data, flags = get_json_data(cmd_name)
    if flags:
        return set(), dict(), set(), dict, flags
    else:
        set_of_all_flags: Set[str] = get_set_of_all_flags(json_data)
        dict_flag_to_primary_repr: Dict[str, str] = get_dict_flag_to_primary_repr(json_data)
        set_of_all_options: Set[str] = get_set_of_all_options(json_data)
        dict_option_to_primary_repr: Dict[str, str] = get_dict_option_to_primary_repr(json_data)
        return set_of_all_flags, dict_flag_to_primary_repr, set_of_all_options, dict_option_to_primary_repr, flags


def default_process_when_default_json_is_used(parsed_elements_list: List[str]) -> \
        Tuple[List[FlagOption], List[Operand]]:
    flag_option_list: List[FlagOption] = []
    operand_list: List[Operand] = []
    i = 1

    while i < len(parsed_elements_list):
        potential_flag_or_option = parsed_elements_list[i]
        if potential_flag_or_option.startswith("-"):
            flag_option_list.append(Flag(potential_flag_or_option))
        else:
            operand_list.append(Operand(potential_flag_or_option))
        i += 1

    return flag_option_list, operand_list


def get_set_of_all_flags(json_data) -> Set[str]:
    return get_set_of_all("flag", json_data)


def get_set_of_all_options(json_data) -> Set[str]:
    set_of_all: Set[str] = set()
    for list_of_flags_or_options in json_data["option"]:
        for flag_or_option in list_of_flags_or_options[:-1]:  # off by 1 due to what the argument is
            set_of_all.add(flag_or_option)
    return set_of_all


def get_set_of_all(flag_or_option_str: Literal["flag", "option"], json_data) -> Set[str]:
    set_of_all: Set[str] = set()
    for list_of_flags_or_options in json_data[flag_or_option_str]:
        for flag_or_option in list_of_flags_or_options:
            set_of_all.add(flag_or_option)
    return set_of_all


def get_dict_flag_to_primary_repr(json_data):
    dict_flag_to_primary_repr: Dict[str, str] = dict()
    for list_of_equiv_flag_repr in json_data["flag"]:
        for i in range(1, len(list_of_equiv_flag_repr)):
            dict_flag_to_primary_repr[list_of_equiv_flag_repr[i]] = list_of_equiv_flag_repr[0]
    return dict_flag_to_primary_repr


def get_dict_option_to_primary_repr(json_data):
    dict_option_to_primary_repr: Dict[str, str] = dict()
    for list_of_equiv_flag_repr in json_data["option"]:
        for i in range(1, len(list_of_equiv_flag_repr) - 1):  # last one contains type
            dict_option_to_primary_repr[list_of_equiv_flag_repr[i]] = list_of_equiv_flag_repr[0]
    return dict_option_to_primary_repr


def all_is_individually_flags(potential_flag_or_option, set_of_all_flags):
    if potential_flag_or_option == "" or potential_flag_or_option[0] != '-' or potential_flag_or_option == '-':
        return False
    return all(f'-{split_el}' in set_of_all_flags for split_el in list(potential_flag_or_option[1:]))


def all_but_last_is_individually_flags(potential_flag_or_option, set_of_all_flags, set_of_all_options):
    if potential_flag_or_option == "" or potential_flag_or_option[0] != '-' or potential_flag_or_option == '-':
        return False
    split_el = f'-{potential_flag_or_option[-1]}'
    if split_el in set_of_all_flags or split_el in set_of_all_options:
        return all(f'-{split_el}' in set_of_all_flags for split_el in list(potential_flag_or_option[1:-1]))
    else:
        return False
