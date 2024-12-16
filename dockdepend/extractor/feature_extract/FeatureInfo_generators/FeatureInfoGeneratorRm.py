from dockdepend.extractor.feature_extract.FeatureInfo_generators.FeatureInfoGenerator_Interface import \
    FeatureInfoGeneratorInterface


class FeatureInfoGeneratorRm(FeatureInfoGeneratorInterface):
    # Which ones do affect input/output?
    # None
    def generate_info(self) -> None:
        self.all_operands_are_io()
