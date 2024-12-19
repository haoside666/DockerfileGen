from graphgen.extractor.feature_extract.FeatureInfo_generators.FeatureInfoGenerator_Interface import \
    FeatureInfoGeneratorInterface


class FeatureInfoGeneratorUniq(FeatureInfoGeneratorInterface):

    # list_of_all_flags = ["-c", "-d", "-D", "-i", "-u", "-z", "--help", "--version"]
    # list_of_all_options = ["--all-repeated", "-f", "--group", "-s", "-w"]

    # Which ones do affect input/output?
    # only the number of operands and flags --help and --version

    def generate_info(self) -> None:
        # tested this with the command, man-page a bit inconclusive with optional OUTPUT
        # assumption that version/help not provided
        if self.get_operand_list_length() == 1:
            self.all_operands_are_other_input()
        elif self.get_operand_list_length() == 2:
            self.all_but_last_operand_is_other_input()
            self.only_last_operand_is_other_output()
        else:
            raise Exception('extra operand for uniq, the 3rd one')
