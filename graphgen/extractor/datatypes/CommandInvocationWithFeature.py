from typing import List, Union
from graphgen.extractor.datatypes.BasicDatatypes import Flag, ArgStringType
from graphgen.extractor.datatypes.BasicDatatypesWithFeature import BaseClassForBasicDatatypesWithFeatureInfo, OptionWithFeature
from graphgen.extractor.datatypes.CommandInvocationFeature import CommandInvocationFeature
from graphgen.extractor.datatypes.AccessKindCommon import WhichClassForFeature
from graphgen.extractor.util_standard import standard_repr, standard_eq


class CommandInvocationWithFeature:
    # TODO: fully substitute by ...Vars and delete this one

    def __init__(self,
                 cmd_name: str,
                 flag_option_list: List[Union[Flag, OptionWithFeature]],
                 operand_list: List[Union[ArgStringType, BaseClassForBasicDatatypesWithFeatureInfo]],
                 ) -> None:
        self.cmd_name: str = cmd_name
        self.flag_option_list: List[Union[Flag, OptionWithFeature]] = flag_option_list
        self.operand_list: List[Union[ArgStringType, BaseClassForBasicDatatypesWithFeatureInfo]] = operand_list

    def __repr__(self):
        return standard_repr(self)

    def __eq__(self, other):
        return standard_eq(self, other)

    def get_options_with_config_input(self):
        only_options: List[OptionWithFeature] = [x for x in self.flag_option_list if isinstance(x, OptionWithFeature)]
        return [x for x in only_options if
                (isinstance(x.option_arg, BaseClassForBasicDatatypesWithFeatureInfo))
                and x.option_arg.access.is_config_input()]

    def get_options_with_config_output(self):
        only_options: List[OptionWithFeature] = [x for x in self.flag_option_list if isinstance(x, OptionWithFeature)]
        return [x for x in only_options if
                (isinstance(x.option_arg, BaseClassForBasicDatatypesWithFeatureInfo))
                and x.option_arg.access.is_config_output()]

    def get_operands_with_user(self) -> List[BaseClassForBasicDatatypesWithFeatureInfo]:
        return [x for x in self.operand_list if
                (isinstance(x, BaseClassForBasicDatatypesWithFeatureInfo))
                and x.feature_class == WhichClassForFeature.USER]

    def get_operands_with_pkg(self) -> List[BaseClassForBasicDatatypesWithFeatureInfo]:
        return [x for x in self.operand_list if
                (isinstance(x, BaseClassForBasicDatatypesWithFeatureInfo))
                and x.feature_class == WhichClassForFeature.PKG]

    def get_operands_with_other(self) -> List[BaseClassForBasicDatatypesWithFeatureInfo]:
        return [x for x in self.operand_list if
                (isinstance(x, BaseClassForBasicDatatypesWithFeatureInfo))
                and x.feature_class == WhichClassForFeature.OTHER]

    def get_operands_with_file(self) -> List[BaseClassForBasicDatatypesWithFeatureInfo]:
        return [x for x in self.operand_list if
                (isinstance(x, BaseClassForBasicDatatypesWithFeatureInfo))
                and x.feature_class == WhichClassForFeature.FILESTD]

    def get_command_feature_info(self) -> CommandInvocationFeature:
        cmd_name: str = self.cmd_name
        input_list: List = []
        output_list: List = []
        pkg_list: List = []
        other_list: List = []
        user_list: List = []
        # 1) handle flagoption list
        only_options: List[OptionWithFeature] = [x for x in self.flag_option_list if isinstance(x, OptionWithFeature)]
        for x in only_options:
            option_arg = x.option_arg
            if isinstance(option_arg, BaseClassForBasicDatatypesWithFeatureInfo):
                if option_arg.feature_class == WhichClassForFeature.FILESTD:
                    if option_arg.access.is_any_input():
                        input_list.append(option_arg.name)
                    elif option_arg.access.is_any_output():
                        output_list.append(option_arg.name)
        # 2) handle operand list
        for x in self.operand_list:
            if isinstance(x, BaseClassForBasicDatatypesWithFeatureInfo):
                if x.feature_class == WhichClassForFeature.FILESTD:
                    if x.access.is_any_input():
                        input_list.append(x.name)
                    if x.access.is_any_output():
                        output_list.append(x.name)
                elif x.feature_class == WhichClassForFeature.USER:
                    user_list.append(x.name)
                elif x.feature_class == WhichClassForFeature.PKG:
                    pkg_list.append(x.name)
                elif x.feature_class == WhichClassForFeature.OTHER:
                    other_list.append(x.name)
        return CommandInvocationFeature(cmd_name, input_list, output_list, pkg_list, other_list, user_list)
