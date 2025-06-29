from graphgen.extractor.feature_extract.FeatureInfo_generators.FeatureInfoGenerator_Interface import \
    FeatureInfoGeneratorInterface


class FeatureInfoGeneratorLn(FeatureInfoGeneratorInterface):
    # Which ones do affect input/output?
    #

    def generate_info(self) -> None:
        operand_list = self.cmd_inv_after_io.operand_list
        if self.does_flag_option_list_contain_specific_parameter("-t"):
            assert (len(operand_list) == 1)
            self.only_first_operand_is_other_input()
        else:
            if len(operand_list) > 1:
                self.all_but_last_operand_is_other_input()
                self.only_last_operand_is_other_output()
            else:
                self.all_operands_are_other_output()

