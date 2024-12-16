from typing import List, Union, Optional
from dockdepend.extractor.datatypes.BasicDatatypes import Flag, ArgStringType
from dockdepend.extractor import OptionWithIO, FileNameOrStdDescriptorWithIOInfo, \
    FileNameWithIOInfo, \
    StdDescriptorWithIOInfo
from dockdepend.extractor.datatypes.CommandInvocationFeature import CommandInvocationFeature
from dockdepend.extractor.util_standard import standard_repr, standard_eq


class CommandInvocationWithIO:
    # TODO: fully substitute by ...Vars and delete this one

    def __init__(self,
                 cmd_name: str,
                 flag_option_list: List[Union[Flag, OptionWithIO]],
                 operand_list: List[Union[ArgStringType, FileNameOrStdDescriptorWithIOInfo]],
                 implicit_use_of_streaming_input: Optional[FileNameOrStdDescriptorWithIOInfo],
                 implicit_use_of_streaming_output: Optional[FileNameOrStdDescriptorWithIOInfo],
                 ) -> None:
        self.cmd_name: str = cmd_name
        self.flag_option_list: List[Union[Flag, OptionWithIO]] = flag_option_list
        self.operand_list: List[Union[ArgStringType, FileNameOrStdDescriptorWithIOInfo]] = operand_list
        self.implicit_use_of_streaming_input: Optional[
            FileNameOrStdDescriptorWithIOInfo] = implicit_use_of_streaming_input
        self.implicit_use_of_streaming_output: Optional[
            FileNameOrStdDescriptorWithIOInfo] = implicit_use_of_streaming_output

    def __repr__(self):
        return standard_repr(self)

    def __eq__(self, other):
        return standard_eq(self, other)

    # for test cases:
    def get_operands_with_config_input(self) -> List[Union[ArgStringType, FileNameOrStdDescriptorWithIOInfo]]:
        return [x for x in self.operand_list if
                (isinstance(x, FileNameWithIOInfo) or isinstance(x, StdDescriptorWithIOInfo))
                and x.access.is_config_input()]

    def get_operands_with_stream_input(self) -> List[FileNameOrStdDescriptorWithIOInfo]:
        return [x for x in self.operand_list if
                (isinstance(x, FileNameWithIOInfo) or isinstance(x, StdDescriptorWithIOInfo))
                and x.access.is_stream_input()]

    def get_operands_with_other_input(self) -> List[FileNameOrStdDescriptorWithIOInfo]:
        return [x for x in self.operand_list if
                (isinstance(x, FileNameWithIOInfo) or isinstance(x, StdDescriptorWithIOInfo))
                and x.access.is_other_input()]

    def get_operands_with_stream_output(self) -> List[FileNameOrStdDescriptorWithIOInfo]:
        return [x for x in self.operand_list if
                (isinstance(x, FileNameWithIOInfo) or isinstance(x, StdDescriptorWithIOInfo))
                and x.access.is_stream_output()]

    def get_operands_with_other_output(self) -> List[FileNameOrStdDescriptorWithIOInfo]:
        return [x for x in self.operand_list if
                (isinstance(x, FileNameWithIOInfo) or isinstance(x, StdDescriptorWithIOInfo))
                and x.access.is_other_output()]

    def get_options_with_other_output(self) -> List[OptionWithIO]:
        only_options: List[OptionWithIO] = [x for x in self.flag_option_list if isinstance(x, OptionWithIO)]
        return [x for x in only_options if
                (isinstance(x.option_arg, FileNameWithIOInfo) or isinstance(x.option_arg, StdDescriptorWithIOInfo))
                and x.option_arg.access.is_other_output()]

    def get_options_with_config_output(self) -> List[OptionWithIO]:
        only_options: List[OptionWithIO] = [x for x in self.flag_option_list if isinstance(x, OptionWithIO)]
        return [x for x in only_options if
                (isinstance(x.option_arg, FileNameWithIOInfo) or isinstance(x.option_arg, StdDescriptorWithIOInfo))
                and x.option_arg.access.is_config_output()]

    def get_options_with_config_input(self) -> List[OptionWithIO]:
        only_options: List[OptionWithIO] = [x for x in self.flag_option_list if isinstance(x, OptionWithIO)]
        return [x for x in only_options if
                (isinstance(x.option_arg, FileNameWithIOInfo) or isinstance(x.option_arg, StdDescriptorWithIOInfo))
                and x.option_arg.access.is_config_input()]

    def get_command_feature_info(self) -> CommandInvocationFeature:
        cmd_name: str = self.cmd_name
        input_list: List = []
        output_list: List = []
        # 1) handle flagoption list
        only_options: List[OptionWithIO] = [x for x in self.flag_option_list if isinstance(x, OptionWithIO)]
        for x in only_options:
            option_arg = x.option_arg
            if isinstance(option_arg, FileNameWithIOInfo) or isinstance(option_arg, StdDescriptorWithIOInfo):
                if option_arg.access.is_any_input():
                    input_list.append(option_arg.get_name())
                elif option_arg.access.is_any_output():
                    output_list.append(option_arg.get_name())
        # 2) handle operand list
        for x in self.operand_list:
            if isinstance(x, FileNameWithIOInfo) or isinstance(x, StdDescriptorWithIOInfo):
                if x.access.is_any_input():
                    input_list.append(x.get_name())
                if x.access.is_any_output():
                    output_list.append(x.get_name())
        return CommandInvocationFeature(cmd_name, input_list, output_list, [], [], [])
