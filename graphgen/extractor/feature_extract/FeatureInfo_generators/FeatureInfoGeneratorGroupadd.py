from graphgen.extractor.feature_extract.FeatureInfo_generators.FeatureInfoGenerator_Interface import \
    FeatureInfoGeneratorInterface
from graphgen.extractor.datatypes.AccessKindCommon import WhichClassForFeature

class FeatureInfoGeneratorGroupadd(FeatureInfoGeneratorInterface):
    def generate_info(self) -> None:
        self.all_operands_are_user()
        operand_list = self.cmd_inv_after_io.operand_list
        user_name = operand_list[-1].get_name()
        self.add_one_element_to_operand_list(user_name, (WhichClassForFeature.OTHER, None))
