from dockdepend.extractor.feature_extract.FeatureInfo_generators.FeatureInfoGenerator_Interface import \
    FeatureInfoGeneratorInterface


class FeatureInfoGeneratorChmod(FeatureInfoGeneratorInterface):
    # Which ones do affect input/output?
    #

    def generate_info(self) -> None:
        if self.does_flag_option_list_contain_specific_parameter("--reference"):
            self.all_operands_are_other_input()
        else:
            self.all_but_first_operand_is_other_input()
