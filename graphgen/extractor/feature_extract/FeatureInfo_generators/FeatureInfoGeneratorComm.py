from graphgen.extractor.feature_extract.FeatureInfo_generators.FeatureInfoGenerator_Interface import \
    FeatureInfoGeneratorInterface


class FeatureInfoGeneratorComm(FeatureInfoGeneratorInterface):
    # for details on what the functions do, check comments in its super class InputOutputInfoGeneratorInterface

    # list_of_all_flags = ["-1", "-2", "-3", "--check-order", "--nocheck-order", "--total", "-z", "--help", "--version"]
    # list_of_all_options = ["--output-delimiter"]

    # Which ones do affect input/output?
    # none

    def generate_info(self) -> None:
        assert (self.get_operand_list_length() == 2)  # needs two files to compare;
        self.all_operands_are_other_input()
