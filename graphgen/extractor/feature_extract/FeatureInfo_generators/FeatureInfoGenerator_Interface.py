from typing import List, Tuple, Union, Literal, Dict
from graphgen.extractor.config.definitions import INDICATORS_FOR_FILENAMES
from graphgen.extractor.datatypes.BasicDatatypes import Flag, Option, FlagOption, Operand
from graphgen.extractor.datatypes.AccessKindCommon import AccessKindCommon, get_access_from_string, WhichClassForFeature
from graphgen.extractor.datatypes.CommandInvocationInitial import CommandInvocationInitial
from graphgen.extractor.datatypes.CommandInvocationAfterIOChange import CommandInvocationAfterIOChange
from abc import ABC, abstractmethod
from graphgen.extractor.feature_extract.datatypes.FeatureInfo import FeatureInfo
from graphgen.extractor.parser.util_parser import get_json_data


class FeatureInfoGeneratorInterface(ABC):
    # here, we only need to specify information about operands and implicitly used resources
    # information about option arguments are provided by parsing infrastructure
    # ASSUMPTION: No implicit information should be exploited since internal implementation may change

    def __init__(self, cmd_invocation: CommandInvocationInitial, pipe: str) -> None:
        self.cmd_inv_after_io: CommandInvocationAfterIOChange = CommandInvocationAfterIOChange(cmd_invocation)
        self.pipe: str = pipe
        flagoption_list_typer: List[Union[Tuple[Literal[WhichClassForFeature.FILESTD], AccessKindCommon],
                                          Tuple[Literal[WhichClassForFeature.ARGSTRING], None],
                                          Tuple[Literal[WhichClassForFeature.PLAINSTRING], None]]] \
            = self.get_flagoption_list_typer_for_specific_list()
        self.feature_info: FeatureInfo = FeatureInfo(
            flagoption_list_typer=flagoption_list_typer,
            number_of_operands=len(cmd_invocation.operand_list)
        )

    @abstractmethod
    def generate_info(self) -> None:
        pass

    def get_info(self) -> FeatureInfo:
        return self.feature_info

    def get_pipe(self) -> str:
        return self.pipe

    def reset_flagoption_list_by_index(self, index: int, kind: AccessKindCommon):
        self.feature_info.reset_flagoption_list_by_index_with_kind_equal_config_input_or_output(index, kind)

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

    def does_first_operand_equal_arg(self, arg) -> bool:
        first_operand_name = self.get_first_operand_name_as_string()
        return arg == first_operand_name

    def does_first_operand_contain(self, list_names: List[str]) -> bool:
        first_operand_name = self.get_first_operand_name_as_string()
        return first_operand_name in list_names

    def add_one_element_to_operand_list(self, operand_arg,
                                        typer: Union[Tuple[Literal[WhichClassForFeature.FILESTD], AccessKindCommon],
                                                     Tuple[Literal[WhichClassForFeature.USER], None],
                                                     Tuple[Literal[WhichClassForFeature.PKG], None],
                                                     Tuple[Literal[WhichClassForFeature.OTHER], None],
                                                     Tuple[Literal[WhichClassForFeature.ARGSTRING], None]]):
        self.cmd_inv_after_io.operand_list.append(Operand(operand_arg))
        self.feature_info.operand_list_typer.append(typer)

    def get_flagoption_list_typer_for_specific_list(self) -> \
            List[Union[Tuple[Literal[WhichClassForFeature.FILESTD], AccessKindCommon],
                       Tuple[Literal[WhichClassForFeature.ARGSTRING], None],
                       Tuple[Literal[WhichClassForFeature.PLAINSTRING], None]]]:
        dict_option_to_class_for_arg: Dict[str, Union[Tuple[Literal[WhichClassForFeature.FILESTD], AccessKindCommon],
                                                      Tuple[Literal[WhichClassForFeature.ARGSTRING], None]]] \
            = self.get_dict_option_to_class_for_arg()
        flagoption_list_typer = []
        for flagoption in self.cmd_inv_after_io.flag_option_list:
            if isinstance(flagoption, Flag):
                flagoption_list_typer.append((WhichClassForFeature.PLAINSTRING, None))
            elif isinstance(flagoption, Option):
                flagoption_list_typer.append(dict_option_to_class_for_arg[flagoption.get_name()])
            else:
                raise Exception("neither Flag nor Option")
        return flagoption_list_typer

    def get_dict_option_to_class_for_arg(self) -> Dict[
        str, Union[Tuple[Literal[WhichClassForFeature.FILESTD], AccessKindCommon],
                   Tuple[Literal[WhichClassForFeature.ARGSTRING], None]]]:
        dict_option_to_class_for_arg: Dict[str, Union[Tuple[Literal[WhichClassForFeature.FILESTD], AccessKindCommon],
                                                      Tuple[Literal[WhichClassForFeature.ARGSTRING], None]]] = dict()
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
                    access: AccessKindCommon = get_access_from_string(option_arg_access_str)
                    if option_arg_type in INDICATORS_FOR_FILENAMES:
                        # for now, we do not allow to have '-' for stdin in option arguments
                        dict_option_to_class_for_arg[option_name] = (WhichClassForFeature.FILESTD, access)
                    else:
                        dict_option_to_class_for_arg[option_name] = (WhichClassForFeature.ARGSTRING, None)
                else:
                    option_arg_type: str = option_arg_info
                    if option_arg_type in INDICATORS_FOR_FILENAMES:
                        print(option_arg_type)
                        # filenames need to declare access pattern, no default
                        assert (not option_arg_type in INDICATORS_FOR_FILENAMES)

                    dict_option_to_class_for_arg[option_name] = (WhichClassForFeature.ARGSTRING, None)
            return dict_option_to_class_for_arg

    ## Library functions
    def all_operands_are_other_input(self) -> None:
        self.feature_info.all_operands_are_other_input()

    def all_operands_are_other_output(self) -> None:
        self.feature_info.all_operands_are_other_output()

    def all_operands_are_io(self) -> None:
        self.feature_info.all_operands_are_io()

    def all_operands_are_user(self) -> None:
        self.feature_info.all_operands_are_user()

    def all_operands_are_pkg(self) -> None:
        self.feature_info.all_operands_are_pkg()

    def all_operands_are_other(self) -> None:
        self.feature_info.all_operands_are_other()

    def all_but_first_operand_is_other_input(self) -> None:
        self.feature_info.all_but_first_operand_is_other_input()

    def all_but_first_operand_is_io(self) -> None:
        self.feature_info.all_but_first_operand_is_io()

    def all_but_first_operand_is_other_output(self) -> None:
        self.feature_info.all_but_first_operand_is_other_output()

    def all_but_last_operand_is_other_input(self) -> None:
        self.feature_info.all_but_last_operand_is_other_input()

    def all_but_first_operand_is_pkg(self) -> None:
        self.feature_info.all_but_first_operand_is_pkg()

    def only_last_operand_is_user(self) -> None:
        self.feature_info.only_last_operand_is_user()

    def only_last_operand_is_other(self) -> None:
        self.feature_info.only_last_operand_is_other()

    def only_last_operand_is_other_output(self) -> None:
        self.feature_info.only_last_operand_is_other_output()

    def only_last_operand_is_io(self) -> None:
        self.feature_info.only_last_operand_is_io()

    def only_first_operand_is_other_input(self) -> None:
        self.feature_info.only_first_operand_is_other_input()

    def only_first_operand_is_other_output(self) -> None:
        self.feature_info.only_first_operand_is_other_output()

    def set_operand_element_by_index(self, index,
                                     typer: Union[Tuple[Literal[WhichClassForFeature.FILESTD], AccessKindCommon],
                                                  Tuple[Literal[WhichClassForFeature.USER], None],
                                                  Tuple[Literal[WhichClassForFeature.PKG], None],
                                                  Tuple[Literal[WhichClassForFeature.OTHER], None],
                                                  Tuple[Literal[WhichClassForFeature.ARGSTRING], None]]) -> None:
        self.feature_info.set_operand_element_by_index(index, typer)

    def strip_startswith_is_hyphen_in_operand_list(self):
        operand_list = self.cmd_inv_after_io.operand_list
        length = len(operand_list)
        del_list = []
        for index in range(length):
            operand = operand_list[index].name
            if operand.startswith("-"):
                del_list.append(index)
        self.cmd_inv_after_io.operand_list = remove_elements_by_index(operand_list, del_list)
        self.feature_info.operand_list_typer = remove_elements_by_index(self.feature_info.operand_list_typer, del_list)


def remove_elements_by_index(original_index: List, index_list: List):
    return [original_index[i] for i in range(len(original_index)) if i not in index_list]
