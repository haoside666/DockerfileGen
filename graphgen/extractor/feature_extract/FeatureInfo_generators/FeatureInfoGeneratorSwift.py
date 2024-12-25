from graphgen.extractor.feature_extract.FeatureInfo_generators.FeatureInfoGenerator_Interface import \
    FeatureInfoGeneratorInterface
from graphgen.extractor.datatypes.AccessKindCommon import WhichClassForFeature, make_other_output, make_other_input


class FeatureInfoGeneratorSwift(FeatureInfoGeneratorInterface):
    def generate_info(self) -> None:
        if self.get_operand_list_length() > 0:
        #     self.all_but_first_operands_is_pkg()
            if self.does_first_operand_equal_arg("build"):
                self.add_one_element_to_operand_list("Package.resolved",
                                                     (WhichClassForFeature.FILESTD, make_other_output()))
            elif self.does_first_operand_equal_arg("package"):
                self.add_one_element_to_operand_list("Package.resolved", (WhichClassForFeature.FILESTD, make_other_input()))
            self.add_one_element_to_operand_list("swift", (WhichClassForFeature.PKG, None))
