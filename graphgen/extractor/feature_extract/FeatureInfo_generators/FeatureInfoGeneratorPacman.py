from graphgen.extractor.feature_extract.FeatureInfo_generators.FeatureInfoGenerator_Interface import \
    FeatureInfoGeneratorInterface


class FeatureInfoGeneratorPacman(FeatureInfoGeneratorInterface):
    def generate_info(self) -> None:
        if self.does_flag_option_list_contain_at_least_one_of(["-F", "-U"]):
            self.all_operands_are_other_input()
        else:
            self.all_operands_are_pkg()
