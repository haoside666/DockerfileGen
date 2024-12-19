from graphgen.extractor.feature_extract.FeatureInfo_generators.FeatureInfoGenerator_Interface import \
    FeatureInfoGeneratorInterface
from graphgen.extractor.datatypes.AccessKindCommon import WhichClassForFeature, make_other_input


class FeatureInfoGeneratorYarn(FeatureInfoGeneratorInterface):
    def generate_info(self) -> None:
        self.strip_startswith_is_hyphen_in_operand_list()
        self.add_one_element_to_operand_list("package.json", (WhichClassForFeature.FILESTD, make_other_input()))
        self.add_one_element_to_operand_list("yarn.lock", (WhichClassForFeature.FILESTD, make_other_input()))
        self.add_one_element_to_operand_list("Yarn", (WhichClassForFeature.PKG, None))
