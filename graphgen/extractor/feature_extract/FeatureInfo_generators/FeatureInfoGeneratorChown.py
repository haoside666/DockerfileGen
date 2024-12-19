from graphgen.extractor.feature_extract.FeatureInfo_generators.FeatureInfoGenerator_Interface import \
    FeatureInfoGeneratorInterface
from graphgen.extractor.datatypes.AccessKindCommon import WhichClassForFeature


class FeatureInfoGeneratorChown(FeatureInfoGeneratorInterface):
    def generate_info(self) -> None:
        self.strip_startswith_is_hyphen_in_operand_list()
        if self.does_flag_option_list_contain_specific_parameter("--reference"):
            self.all_operands_are_other_input()
        else:
            if self.get_operand_list_length() > 0:
                first_operand = self.get_first_operand_name_as_string().replace(".", "")
                user_name = first_operand.split(":")[0]
                self.all_but_first_operand_is_other_input()
                self.add_one_element_to_operand_list(user_name, (WhichClassForFeature.OTHER, None))
