from dockdepend.extractor.feature_extract.FeatureInfo_generators.FeatureInfoGenerator_Interface import \
    FeatureInfoGeneratorInterface


class FeatureInfoGeneratorMkfifo(FeatureInfoGeneratorInterface):

    def generate_info(self) -> None:
        self.all_operands_are_other_output()
