import os

from dockdepend.extractor.feature_extract.FeatureInfo_generators.FeatureInfoGenerator_Interface import \
    FeatureInfoGeneratorInterface
from dockdepend.extractor.datatypes.AccessKindCommon import WhichClassForFeature
from dockdepend.extractor.datatypes.BasicDatatypes import Operand
import re


class FeatureInfoGeneratorDpkg(FeatureInfoGeneratorInterface):
    def generate_info(self) -> None:
        self.strip_startswith_is_hyphen_in_operand_list()
        operand_list = self.cmd_inv_after_io.operand_list
        length = len(operand_list)
        for index in range(length):
            operand_arg = operand_list[index].get_name()
            if ".deb" in operand_arg:
                pkg_name = match_pkg_name(operand_arg)
                operand_list[index] = Operand(pkg_name)
                self.set_operand_element_by_index(index, (WhichClassForFeature.PKG, None))


def match_pkg_name(pkg_string: str) -> str:
    name = os.path.basename(pkg_string)
    pattern = r'^[a-zA-Z-]+'
    match_result = re.match(pattern, name)
    if match_result:
        pkg_name = match_result.group()
        return pkg_name
    else:
        return name.replace(".deb", "")
