from dockdepend.extractor.feature_extract.FeatureInfo_generators.FeatureInfoGenerator_Interface import \
    FeatureInfoGeneratorInterface


class FeatureInfoGeneratorCp(FeatureInfoGeneratorInterface):

    # Which ones do affect input/output?
    #

    def generate_info(self) -> None:
        # -T shall treat destination as file, not directory, not considered currently
        # -t gives destination directory as an argument to option and determines how operands are interpreted
        if self.does_flag_option_list_contain_specific_parameter("-t"):
            self.all_operands_are_other_input()
        else:
            self.all_but_last_operand_is_other_input()
            self.only_last_operand_is_other_output()
