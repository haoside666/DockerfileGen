from graphgen.extractor.feature_extract.FeatureInfo_generators.FeatureInfoGenerator_Interface import \
    FeatureInfoGeneratorInterface
from graphgen.extractor.datatypes.AccessKindCommon import WhichClassForFeature, make_other_input


class FeatureInfoGeneratorDockerPhp(FeatureInfoGeneratorInterface):
    def generate_info(self) -> None:
        self.add_one_element_to_operand_list("php", (WhichClassForFeature.PKG, None))
        if self.cmd_inv_after_io.does_operand_list_contain(["gd"]):
            self.add_one_element_to_operand_list("/etc", (WhichClassForFeature.FILESTD, make_other_input()))


