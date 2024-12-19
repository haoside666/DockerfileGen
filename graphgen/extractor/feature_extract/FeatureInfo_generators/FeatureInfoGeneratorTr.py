from graphgen.extractor.feature_extract.FeatureInfo_generators.FeatureInfoGenerator_Interface import \
    FeatureInfoGeneratorInterface


class FeatureInfoGeneratorTr(FeatureInfoGeneratorInterface):

    # list_of_all_flags = ["-c", "-d", "-s", "-t", "--help", "--version",
    # list_of_all_options = []

    # Which ones do affect input/output?
    # none, takes from stdin and prints to stdout and no way to suppress output

    def generate_info(self) -> None:
        pass
