from graphgen.extractor.feature_extract.FeatureInfo_generators.FeatureInfoGenerator_Interface import \
    FeatureInfoGeneratorInterface


class FeatureInfoGeneratorSort(FeatureInfoGeneratorInterface):

    # Which ones do affect input/output?

    def generate_info(self) -> None:
        # self.set_multiple_inputs_possible()

        if self.get_operand_list_length() != 0:
            self.all_operands_are_other_input()
