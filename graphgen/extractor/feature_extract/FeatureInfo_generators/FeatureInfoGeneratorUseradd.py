from graphgen.extractor.feature_extract.FeatureInfo_generators.FeatureInfoGenerator_Interface import \
    FeatureInfoGeneratorInterface
from graphgen.extractor.datatypes.AccessKindCommon import WhichClassForFeature


class FeatureInfoGeneratorUseradd(FeatureInfoGeneratorInterface):
    def generate_info(self) -> None:
        if self.get_operand_list_length() > 0:
            self.all_but_last_operand_is_other_input()
            self.only_last_operand_is_user()
            operand_list = self.cmd_inv_after_io.operand_list
            user_name = operand_list[-1].get_name()
            self.add_one_element_to_operand_list(user_name, (WhichClassForFeature.OTHER, None))
