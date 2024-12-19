from graphgen.extractor.feature_extract.FeatureInfo_generators.FeatureInfoGenerator_Interface import \
    FeatureInfoGeneratorInterface
from graphgen.extractor.datatypes.AccessKindCommon import WhichClassForFeature, make_other_input, make_other_io


class FeatureInfoGeneratorBundle(FeatureInfoGeneratorInterface):
    def generate_info(self) -> None:
        self.strip_startswith_is_hyphen_in_operand_list()
        if self.get_operand_list_length() > 0 and self.does_first_operand_contain(["install"]):
            self.add_one_element_to_operand_list("Gemfile", (WhichClassForFeature.FILESTD, make_other_input()))
            self.add_one_element_to_operand_list("Gemfile.lock", (WhichClassForFeature.FILESTD, make_other_io()))
        else:
            self.add_one_element_to_operand_list(".", (WhichClassForFeature.FILESTD, make_other_input()))
        self.add_one_element_to_operand_list("ruby", (WhichClassForFeature.PKG, None))
        self.add_one_element_to_operand_list("bundle", (WhichClassForFeature.PKG, None))
