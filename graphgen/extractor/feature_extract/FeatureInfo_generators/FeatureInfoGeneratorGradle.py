from graphgen.extractor.feature_extract.FeatureInfo_generators.FeatureInfoGenerator_Interface import \
    FeatureInfoGeneratorInterface
from graphgen.extractor.datatypes.AccessKindCommon import WhichClassForFeature, make_other_io


class FeatureInfoGeneratorGradle(FeatureInfoGeneratorInterface):
    def generate_info(self) -> None:
        self.strip_startswith_is_hyphen_in_operand_list()
        operand_list = self.cmd_inv_after_io.operand_list
        length = len(operand_list)
        for index in range(length):
            operand = operand_list[index].get_name()
            if "/" in operand or "." in operand:
                self.set_operand_element_by_index(index,
                                                  (WhichClassForFeature.FILESTD, make_other_io()))
        self.add_one_element_to_operand_list("gradle", (WhichClassForFeature.PKG, None))
