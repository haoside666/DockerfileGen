from dockdepend.extractor.feature_extract.FeatureInfo_generators.FeatureInfoGenerator_Interface import \
    FeatureInfoGeneratorInterface
from dockdepend.extractor.datatypes.AccessKindCommon import WhichClassForFeature, make_other_input


class FeatureInfoGeneratorPhp(FeatureInfoGeneratorInterface):
    def generate_info(self) -> None:
        self.strip_startswith_is_hyphen_in_operand_list()
        operand_list = self.cmd_inv_after_io.operand_list
        length = len(operand_list)
        if length > 0:
            self.only_first_operand_is_other_input()
        for index in range(1, length):
            operand = operand_list[index].get_name()
            if "/" in operand:
                self.set_operand_element_by_index(index,
                                                  (WhichClassForFeature.FILESTD, make_other_input()))
        self.add_one_element_to_operand_list("php", (WhichClassForFeature.PKG, None))
