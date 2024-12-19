from graphgen.extractor.datatypes.AccessKindCommon import AccessKindCommon, WhichClassForFeature
from graphgen.extractor.datatypes.BasicDatatypes import ArgStringType
from typing import Union, Optional


class BaseClassForBasicDatatypesWithFeatureInfo:
    def __init__(self, name: str, feature_class: WhichClassForFeature, access: Optional[AccessKindCommon]) -> None:
        self.name = name
        self.feature_class = feature_class
        self.access = access


class OptionWithFeature:
    def __init__(self, name: str, option_arg: Union[BaseClassForBasicDatatypesWithFeatureInfo, ArgStringType]) -> None:
        self.option_name: str = name
        self.option_arg: Union[BaseClassForBasicDatatypesWithFeatureInfo, ArgStringType] = option_arg

    def get_name(self) -> str:
        return self.option_name

    def get_arg(self) -> Union[BaseClassForBasicDatatypesWithFeatureInfo, ArgStringType]:
        return self.option_arg


class OperandWithFeature:
    def __init__(self, name: BaseClassForBasicDatatypesWithFeatureInfo) -> None:
        self.name = name

    def get_name(self) -> BaseClassForBasicDatatypesWithFeatureInfo:
        return self.name
