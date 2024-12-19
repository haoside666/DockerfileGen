from graphgen.extractor.feature_extract.FeatureInfo_generators.FeatureInfoGenerator_Interface import \
    FeatureInfoGeneratorInterface
from graphgen.extractor.datatypes.AccessKindCommon import WhichClassForFeature


class FeatureInfoGeneratorGem(FeatureInfoGeneratorInterface):
    def generate_info(self) -> None:
        self.add_one_element_to_operand_list("ruby", (WhichClassForFeature.PKG, None))
        self.add_one_element_to_operand_list("gem", (WhichClassForFeature.PKG, None))
