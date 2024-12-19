from typing import List, Tuple, Union, Literal, Dict
from graphgen.extractor.config.definitions import INDICATORS_FOR_FILENAMES
from graphgen.extractor.datatypes.BasicDatatypes import Flag, Option, WhichClassForArg, FlagOption, Operand
from graphgen.extractor import AccessKind, get_access_from_string
from graphgen.extractor.datatypes.CommandInvocationInitial import CommandInvocationInitial
from graphgen.extractor.datatypes.CommandInvocationAfterIOChange import CommandInvocationAfterIOChange
from graphgen.extractor import CommandInvocationWithIO
from abc import ABC, abstractmethod
from graphgen.extractor import InputOutputInfo
from graphgen.extractor.parser.util_parser import get_json_data


class InputOutputInfoGeneratorInterface(ABC):
    # here, we only need to specify information about operands and implicitly used resources
    # information about option arguments are provided by parsing infrastructure
    # ASSUMPTION: No implicit information should be exploited since internal implementation may change

    def __init__(self, cmd_invocation: CommandInvocationInitial, pipe: str) -> None:
        self.cmd_inv_after_io: CommandInvocationAfterIOChange = CommandInvocationAfterIOChange(cmd_invocation)
        self.pipe: str = pipe
        flagoption_list_typer: List[Union[Tuple[Literal[WhichClassForArg.FILESTD], AccessKind],
                                          Tuple[Literal[WhichClassForArg.ARGSTRING], None],
                                          Tuple[Literal[WhichClassForArg.PLAINSTRING], None]]] \
            = self.get_flagoption_list_typer_for_specific_list()
        self.input_output_info: InputOutputInfo = InputOutputInfo(
            flagoption_list_typer=flagoption_list_typer,
            number_of_operands=len(cmd_invocation.operand_list)
        )

    @abstractmethod
    def generate_info(self) -> None:
        pass

    def get_info(self) -> InputOutputInfo:
        return self.input_output_info

    def get_pipe(self) -> str:
        return self.pipe

    def reset_flagoption_list_by_index(self, index: int, kind: AccessKind):
        self.input_output_info.reset_flagoption_list_by_index_with_kind_equal_config_input_or_output(index, kind)

    def get_cmd_inv_after_io(self) -> CommandInvocationAfterIOChange:
        return self.cmd_inv_after_io

    def get_specific_option_by_specific_parameter(self, parameter_name: str) -> Option:
        for flagoption in self.cmd_inv_after_io.flag_option_list:
            if isinstance(flagoption, Option) and flagoption.get_name() == parameter_name:
                return flagoption

    def get_index_by_flag_option_name(self, parameter_name: str) -> int:
        for index in range(len(self.cmd_inv_after_io.flag_option_list)):
            flagoption = self.cmd_inv_after_io.flag_option_list[index]
            if isinstance(flagoption, Option) and flagoption.get_name() == parameter_name:
                return index
        return -1

    def does_flag_option_list_contain_at_least_one_of(self, list_names: List[str]) -> bool:
        return len(self.get_flag_option_list_filtered_with(list_names)) > 0

    def does_flag_option_list_contain_specific_parameter(self, parameter_name: str) -> bool:
        return parameter_name in [flagoption.get_name() for flagoption in self.cmd_inv_after_io.flag_option_list]

    def get_flag_option_list_filtered_with(self, list_names: List[str]) -> List[FlagOption]:
        return [flagoption for flagoption in self.cmd_inv_after_io.flag_option_list if
                flagoption.get_name() in list_names]

    def get_operand_list_length(self):
        return len(self.cmd_inv_after_io.operand_list)

    def get_first_operand_name_as_string(self):
        # assumes that it is of type config
        first_operand = self.cmd_inv_after_io.operand_list[0]
        first_operand_arg = first_operand.get_name()
        first_operand_name = str(first_operand_arg)
        return first_operand_name

    def does_first_operand_start_with(self, arg):
        first_operand_name = self.get_first_operand_name_as_string()
        return first_operand_name.startswith(arg)

    def does_first_operand_contain(self, arg):
        first_operand_name = self.get_first_operand_name_as_string()
        return (arg in first_operand_name)

    def get_cmd_inv_with_io(self, cmd_inv_after_io: CommandInvocationAfterIOChange) -> CommandInvocationWithIO:
        return self.input_output_info.apply_input_output_info_to_command_invocation(cmd_inv_after_io)

    def get_flagoption_list_typer_for_specific_list(self) -> \
            List[Union[Tuple[Literal[WhichClassForArg.FILESTD], AccessKind],
                       Tuple[Literal[WhichClassForArg.ARGSTRING], None],
                       Tuple[Literal[WhichClassForArg.PLAINSTRING], None]]]:
        dict_option_to_class_for_arg: Dict[str, Union[Tuple[Literal[WhichClassForArg.FILESTD], AccessKind],
                                                      Tuple[Literal[WhichClassForArg.ARGSTRING], None]]] \
            = self.get_dict_option_to_class_for_arg()
        flagoption_list_typer = []
        for flagoption in self.cmd_inv_after_io.flag_option_list:
            if isinstance(flagoption, Flag):
                flagoption_list_typer.append((WhichClassForArg.PLAINSTRING, None))
            elif isinstance(flagoption, Option):
                flagoption_list_typer.append(dict_option_to_class_for_arg[flagoption.get_name()])
            else:
                raise Exception("neither Flag nor Option")
        return flagoption_list_typer

    def get_dict_option_to_class_for_arg(self) -> Dict[str, Union[Tuple[Literal[WhichClassForArg.FILESTD], AccessKind],
                                                                  Tuple[Literal[WhichClassForArg.ARGSTRING], None]]]:
        dict_option_to_class_for_arg: Dict[str, Union[Tuple[Literal[WhichClassForArg.FILESTD], AccessKind],
                                                      Tuple[Literal[WhichClassForArg.ARGSTRING], None]]] = dict()
        json_data, flags = get_json_data(self.cmd_inv_after_io.cmd_name)
        if flags:
            return dict()
        else:
            for option_data in json_data["option"]:
                option_name = option_data[0]
                option_arg_info = option_data[-1]
                # CA whether access info is given
                if isinstance(option_arg_info, list):
                    option_arg_type: str = option_arg_info[0]
                    option_arg_access_str: str = option_arg_info[1]
                    access: AccessKind = get_access_from_string(option_arg_access_str)
                    if option_arg_type in INDICATORS_FOR_FILENAMES:
                        # for now, we do not allow to have '-' for stdin in option arguments
                        dict_option_to_class_for_arg[option_name] = (WhichClassForArg.FILESTD, access)
                    else:
                        dict_option_to_class_for_arg[option_name] = (WhichClassForArg.ARGSTRING, None)
                else:
                    option_arg_type: str = option_arg_info
                    if option_arg_type in INDICATORS_FOR_FILENAMES:
                        print(option_arg_type)
                        # filenames need to declare access pattern, no default
                        assert (not option_arg_type in INDICATORS_FOR_FILENAMES)

                    dict_option_to_class_for_arg[option_name] = (WhichClassForArg.ARGSTRING, None)
            return dict_option_to_class_for_arg

    ## Library functions

    # use default values here as counter-measure for using False as default values in constructor

    def set_implicit_use_of_stdin(self, value: bool = True) -> None:
        self.input_output_info.set_implicit_use_of_stdin(value)

    def set_implicit_use_of_stdout(self, value: bool = True) -> None:
        self.input_output_info.set_implicit_use_of_stdout(value)

    def if_no_operands_given_stdin_implicitly_used(self) -> None:
        if len(self.cmd_inv_after_io.operand_list) == 0:
            self.set_implicit_use_of_stdin(True)

    # forwarded to InputOutputInfo
    # Assumption: streaming inputs are always filenames or stdin
    # Assumption: (streaming) outputs are always filenames or stdout
    def all_operands_are_streaming_inputs(self) -> None:
        self.input_output_info.all_operands_are_streaming_inputs()

    def all_operands_are_other_inputs(self) -> None:
        self.input_output_info.all_operands_are_other_inputs()

    def all_operands_are_streaming_outputs(self) -> None:
        self.input_output_info.all_operands_are_streaming_outputs()

    def all_operands_are_other_outputs(self) -> None:
        self.input_output_info.all_operands_are_other_outputs()

    def all_operands_are_io(self) -> None:
        self.input_output_info.all_operands_are_io()

    def all_but_last_operand_is_other_inputs(self):
        self.input_output_info.all_but_last_operand_is_other_inputs()

    def all_but_last_operand_is_other_outputs(self):
        self.input_output_info.all_but_last_operand_is_other_outputs()

    def all_but_first_operand_is_other_inputs(self) -> None:
        self.input_output_info.all_but_first_operand_is_other_inputs()

    def all_but_first_operand_is_other_outputs(self) -> None:
        self.input_output_info.all_but_first_operand_is_other_outputs()

    def all_but_first_operand_is_io(self) -> None:
        self.input_output_info.all_but_first_operand_is_io()

    def only_last_operand_is_other_input(self):
        self.input_output_info.only_last_operand_is_other_input()

    def only_last_operand_is_other_output(self):
        self.input_output_info.only_last_operand_is_other_output()

    def only_first_operand_is_other_input(self):
        self.input_output_info.only_first_operand_is_other_input()

    def only_first_operand_is_other_output(self):
        self.input_output_info.only_first_operand_is_other_output()

    def set_all_operands_as_config_arg_type_string(self):
        self.input_output_info.set_all_operands_as_config_arg_type_string()

    def set_last_operand_as_config_arg_type_string(self):
        self.input_output_info.set_last_operand_as_config_arg_type_string()

    def set_first_operand_as_config_arg_type_string(self):
        self.input_output_info.set_first_operand_as_config_arg_type_string()

    # only used for xargs
    def set_all_operands_as_arg_string(self):
        self.input_output_info.set_all_operands_as_arg_string()

    # Additional io information to address implicit (default) operation
    def add_one_element_to_operand_list(self, operand_arg: str,
                                        typer: Union[Tuple[Literal[WhichClassForArg.FILESTD], AccessKind],
                                                     Tuple[Literal[WhichClassForArg.ARGSTRING], None],
                                                     Tuple[Literal[WhichClassForArg.PLAINSTRING], None]] =
                                        (WhichClassForArg.ARGSTRING, None)):
        self.cmd_inv_after_io.operand_list.append(Operand(operand_arg))
        self.input_output_info.operand_list_typer.append(typer)
