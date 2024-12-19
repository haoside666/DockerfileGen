from graphgen.extractor.util_standard import standard_repr
from typing import List, Tuple, Union, Literal
from graphgen.extractor.datatypes.AccessKindCommon import AccessKindCommon, WhichClassForFeature, \
    make_other_input, make_other_output, make_other_io
from graphgen.extractor.datatypes.CommandInvocationAfterIOChange import CommandInvocationAfterIOChange
from graphgen.extractor.datatypes.CommandInvocationWithFeature import CommandInvocationWithFeature
from graphgen.extractor.datatypes.BasicDatatypes import Operand, ArgStringType, Flag, Option, FlagOption
from graphgen.extractor.datatypes.BasicDatatypesWithFeature import BaseClassForBasicDatatypesWithFeatureInfo, OptionWithFeature


class FeatureInfo:
    def __init__(self,
                 flagoption_list_typer: List[Union[Tuple[Literal[WhichClassForFeature.FILESTD], AccessKindCommon],
                                                   Tuple[Literal[WhichClassForFeature.PLAINSTRING], None],
                                                   Tuple[Literal[WhichClassForFeature.ARGSTRING], None]]],
                 number_of_operands: int,
                 ) -> None:
        self.flagoption_list_typer: List[Union[Tuple[Literal[WhichClassForFeature.FILESTD], AccessKindCommon],
                                               Tuple[Literal[WhichClassForFeature.PLAINSTRING], None],
                                               Tuple[Literal[WhichClassForFeature.ARGSTRING], None]]] = \
            flagoption_list_typer

        self.operand_list_typer: List[Union[Tuple[Literal[WhichClassForFeature.FILESTD], AccessKindCommon],
                                            Tuple[Literal[WhichClassForFeature.USER], None],
                                            Tuple[Literal[WhichClassForFeature.PKG], None],
                                            Tuple[Literal[WhichClassForFeature.OTHER], None],
                                            Tuple[Literal[WhichClassForFeature.ARGSTRING], None]]] = \
            [(WhichClassForFeature.ARGSTRING, None)] * number_of_operands

    def __repr__(self) -> str:
        return standard_repr(self)

    def reset_flagoption_list_by_index_with_kind_equal_config_input_or_output(self, index: int,
                                                                              kind: AccessKindCommon) -> None:
        assert kind.is_config_input() or kind.is_config_output()
        assert self.flagoption_list_typer[index][1].is_config_input_or_output()
        self.flagoption_list_typer[index] = (WhichClassForFeature.FILESTD, kind)

    def all_operands_are_other_input(self) -> None:
        number_of_operands = len(self.operand_list_typer)
        self.operand_list_typer = [(WhichClassForFeature.FILESTD, make_other_input())] * number_of_operands

    def all_operands_are_other_output(self) -> None:
        number_of_operands = len(self.operand_list_typer)
        self.operand_list_typer = [(WhichClassForFeature.FILESTD, make_other_output())] * number_of_operands

    def all_operands_are_io(self) -> None:
        number_of_operands = len(self.operand_list_typer)
        self.operand_list_typer = [(WhichClassForFeature.FILESTD, make_other_io())] * number_of_operands

    def all_operands_are_user(self) -> None:
        number_of_operands = len(self.operand_list_typer)
        self.operand_list_typer = [(WhichClassForFeature.USER, None)] * number_of_operands

    def all_operands_are_pkg(self) -> None:
        number_of_operands = len(self.operand_list_typer)
        self.operand_list_typer = [(WhichClassForFeature.PKG, None)] * number_of_operands

    def all_operands_are_other(self) -> None:
        number_of_operands = len(self.operand_list_typer)
        self.operand_list_typer = [(WhichClassForFeature.OTHER, None)] * number_of_operands

    def all_but_first_operand_is_other_input(self) -> None:
        original_first_entry = self.operand_list_typer[0]
        self.all_operands_are_other_input()
        self.operand_list_typer[0] = original_first_entry

    def all_but_first_operand_is_io(self) -> None:
        original_first_entry = self.operand_list_typer[0]
        self.all_operands_are_io()
        self.operand_list_typer[0] = original_first_entry

    def all_but_first_operand_is_other_output(self) -> None:
        original_first_entry = self.operand_list_typer[0]
        self.all_operands_are_other_output()
        self.operand_list_typer[0] = original_first_entry

    def all_but_last_operand_is_other_input(self) -> None:
        original_first_entry = self.operand_list_typer[-1]
        self.all_operands_are_other_input()
        self.operand_list_typer[-1] = original_first_entry

    def all_but_first_operand_is_pkg(self) -> None:
        original_first_entry = self.operand_list_typer[0]
        self.all_operands_are_pkg()
        self.operand_list_typer[0] = original_first_entry

    def only_last_operand_is_user(self) -> None:
        self.operand_list_typer[-1] = (WhichClassForFeature.USER, None)

    def only_last_operand_is_other(self) -> None:
        self.operand_list_typer[-1] = (WhichClassForFeature.OTHER, None)

    def only_last_operand_is_other_output(self) -> None:
        self.operand_list_typer[-1] = (WhichClassForFeature.FILESTD, make_other_output())

    def only_last_operand_is_io(self) -> None:
        self.operand_list_typer[-1] = (WhichClassForFeature.FILESTD, make_other_io())

    def only_first_operand_is_other_input(self) -> None:
        self.operand_list_typer[0] = (WhichClassForFeature.FILESTD, make_other_input())

    def only_first_operand_is_other_output(self) -> None:
        self.operand_list_typer[0] = (WhichClassForFeature.FILESTD, make_other_output())

    def set_operand_element_by_index(self, index,
                                     typer: Union[Tuple[Literal[WhichClassForFeature.FILESTD], AccessKindCommon],
                                                  Tuple[Literal[WhichClassForFeature.USER], None],
                                                  Tuple[Literal[WhichClassForFeature.PKG], None],
                                                  Tuple[Literal[WhichClassForFeature.OTHER], None],
                                                  Tuple[Literal[WhichClassForFeature.ARGSTRING], None]]) -> None:
        self.operand_list_typer[index] = typer

    def apply_feature_info_to_command_invocation(self, cmd_inv_after_io: CommandInvocationAfterIOChange) \
            -> CommandInvocationWithFeature:
        # 1) transform flagoption list
        flagoption_list_original: List[FlagOption] = cmd_inv_after_io.flag_option_list
        flagoption_list_with_feature: List[Union[Flag, OptionWithFeature]] = \
            [FeatureInfo.apply_typer_to_flagoption(flagoption, typer) for (flagoption, typer) in
             zip(flagoption_list_original, self.flagoption_list_typer)]
        # 2) transform operand list
        operand_list_original: List[Operand] = cmd_inv_after_io.operand_list
        operand_list_with_feature_full: List[Union[ArgStringType, BaseClassForBasicDatatypesWithFeatureInfo]] = \
            [FeatureInfo.apply_typer_to_arg(operand.get_name(), typer) for (operand, typer) in
             zip(operand_list_original, self.operand_list_typer)]
        # 3) build the command invocation with io and return
        cmd_inv_io_full = CommandInvocationWithFeature(
            cmd_name=cmd_inv_after_io.cmd_name,
            flag_option_list=flagoption_list_with_feature,
            operand_list=operand_list_with_feature_full,
        )
        return cmd_inv_io_full

    @staticmethod
    def apply_typer_to_arg(arg: str,
                           typer: Union[Tuple[Literal[WhichClassForFeature.FILESTD], AccessKindCommon],
                                        Tuple[Literal[WhichClassForFeature.USER], None],
                                        Tuple[Literal[WhichClassForFeature.PKG], None],
                                        Tuple[Literal[WhichClassForFeature.OTHER], None],
                                        Tuple[Literal[WhichClassForFeature.ARGSTRING], None]]) \
            -> Union[ArgStringType, BaseClassForBasicDatatypesWithFeatureInfo]:
        if typer[0] == WhichClassForFeature.FILESTD:
            access: AccessKindCommon = typer[1]
            return BaseClassForBasicDatatypesWithFeatureInfo(arg, WhichClassForFeature.FILESTD, access)
        elif typer[0] == WhichClassForFeature.ARGSTRING:
            return ArgStringType(arg)
        elif typer[0] == WhichClassForFeature.USER:
            return BaseClassForBasicDatatypesWithFeatureInfo(arg, WhichClassForFeature.USER, None)
        elif typer[0] == WhichClassForFeature.PKG:
            return BaseClassForBasicDatatypesWithFeatureInfo(arg, WhichClassForFeature.PKG, None)
        elif typer[0] == WhichClassForFeature.OTHER:
            return BaseClassForBasicDatatypesWithFeatureInfo(arg, WhichClassForFeature.OTHER, None)
        else:
            raise Exception("no valid option for argument type WhichClassForArg: " + str(typer[0]))

    @staticmethod
    def apply_typer_to_flagoption(flagoption: FlagOption,
                                  typer: Union[Tuple[Literal[WhichClassForFeature.FILESTD], AccessKindCommon],
                                               Tuple[Literal[WhichClassForFeature.ARGSTRING], None],
                                               Tuple[Literal[WhichClassForFeature.PLAINSTRING], None]]) \
            -> Union[Flag, OptionWithFeature]:
        if isinstance(flagoption, Flag):
            return flagoption
        elif isinstance(flagoption, Option):
            assert (typer[0] == WhichClassForFeature.FILESTD) or (
                    typer[0] == WhichClassForFeature.ARGSTRING)  # PLAINSTRING only for flags

            option_arg = flagoption.get_arg()
            option_arg_new: Union[ArgStringType, BaseClassForBasicDatatypesWithFeatureInfo] = \
                FeatureInfo.apply_typer_to_arg(option_arg, typer)
            return OptionWithFeature(flagoption.get_name(), option_arg_new)
        else:
            raise Exception("neither flag nor option")
