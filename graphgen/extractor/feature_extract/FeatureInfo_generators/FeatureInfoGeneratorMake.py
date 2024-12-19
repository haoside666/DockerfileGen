from graphgen.extractor.feature_extract.FeatureInfo_generators.FeatureInfoGenerator_Interface import \
    FeatureInfoGeneratorInterface
from graphgen.extractor.datatypes.AccessKindCommon import WhichClassForFeature, make_other_input, make_other_io


class FeatureInfoGeneratorMake(FeatureInfoGeneratorInterface):
    def generate_info(self) -> None:
        self.strip_startswith_is_hyphen_in_operand_list()
        if self.get_operand_list_length() > 0:
            operand_list = self.cmd_inv_after_io.operand_list
            length = len(operand_list)
            for index in range(length):
                operand = operand_list[index].get_name()
                if "/" in operand:
                    self.set_operand_element_by_index(index,
                                                      (WhichClassForFeature.FILESTD, make_other_io()))

        self.add_one_element_to_operand_list("Makefile", (WhichClassForFeature.FILESTD, make_other_input()))
        self.add_one_element_to_operand_list("make", (WhichClassForFeature.PKG, None))
