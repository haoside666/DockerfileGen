from graphgen.extractor.feature_extract.FeatureInfo_generators.FeatureInfoGenerator_Interface import \
    FeatureInfoGeneratorInterface


class FeatureInfoGeneratorTail(FeatureInfoGeneratorInterface):
    # basically the same as for HEAD but man page for TAIL is a bit longer

    # list_of_all_flags = ["-q", "--retry", "-v", "-z", "--help", "--version"]
    # list_of_all_options = ["-c", "-f", "-n", "-max-unchanged-stats", "--pid", "-s"]

    # Which ones do affect input/output?
    # none

    def generate_info(self) -> None:
        self.all_operands_are_other_input()
