from graphgen.extractor.feature_extract.FeatureInfo_generators.FeatureInfoGenerator_Interface import \
    FeatureInfoGeneratorInterface


class FeatureInfoGeneratorTee(FeatureInfoGeneratorInterface):

    def generate_info(self) -> None:
        self.all_operands_are_io()