from dockdepend.extractor.feature_extract.FeatureInfo_generators.FeatureInfoGenerator_Interface import \
    FeatureInfoGeneratorInterface


class FeatureInfoGeneratorAwk(FeatureInfoGeneratorInterface):
    def generate_info(self) -> None:
        ## Does this set -f as configuration input?
        if self.does_flag_option_list_contain_at_least_one_of(["-f"]):
            self.all_operands_are_other_input()
        else:
            self.all_but_first_operand_is_other_input()
