from dockdepend.extractor.feature_extract.FeatureInfo_generators.FeatureInfoGenerator_Interface import \
    FeatureInfoGeneratorInterface


class FeatureInfoGeneratorSed(FeatureInfoGeneratorInterface):

    def generate_info(self) -> None:
        if self.does_flag_option_list_contain_at_least_one_of(["-e", "-f"]):
            if self.does_flag_option_list_contain_specific_parameter("-i"):
                self.all_operands_are_io()
            else:
                self.all_operands_are_other_input()
        else:
            if self.does_flag_option_list_contain_specific_parameter("-i"):
                self.all_but_first_operand_is_io()
            else:
                self.all_but_first_operand_is_other_input()

