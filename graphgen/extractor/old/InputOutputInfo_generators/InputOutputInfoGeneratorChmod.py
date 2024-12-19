from graphgen.extractor.old.InputOutputInfo_generators.InputOutputInfoGenerator_Interface import \
    InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorChmod(InputOutputInfoGeneratorInterface):
    # Which ones do affect input/output?
    #

    def generate_info(self) -> None:
        if self.does_flag_option_list_contain_specific_parameter("--reference"):
            self.all_operands_are_other_inputs()
        else:
            self.all_but_first_operand_is_other_inputs()
