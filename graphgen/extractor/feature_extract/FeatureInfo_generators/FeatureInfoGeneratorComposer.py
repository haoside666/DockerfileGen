from graphgen.extractor.feature_extract.FeatureInfo_generators.FeatureInfoGenerator_Interface import \
    FeatureInfoGeneratorInterface
from graphgen.extractor.datatypes.AccessKindCommon import WhichClassForFeature, make_other_input


class FeatureInfoGeneratorComposer(FeatureInfoGeneratorInterface):
    def generate_info(self) -> None:
        self.strip_startswith_is_hyphen_in_operand_list()
        if self.get_operand_list_length() > 0:
            self.add_one_element_to_operand_list("composer.json", (WhichClassForFeature.FILESTD, make_other_input()))
            self.add_one_element_to_operand_list("composer.lock", (WhichClassForFeature.FILESTD, make_other_input()))

        self.add_one_element_to_operand_list("composer", (WhichClassForFeature.PKG, None))
