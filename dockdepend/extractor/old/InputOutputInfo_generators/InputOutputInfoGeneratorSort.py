from dockdepend.extractor.old.InputOutputInfo_generators.InputOutputInfoGenerator_Interface import \
    InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorSort(InputOutputInfoGeneratorInterface):

    # Which ones do affect input/output?

    def generate_info(self) -> None:
        # self.set_multiple_inputs_possible()
        if not self.does_flag_option_list_contain_at_least_one_of(["-o"]):
            self.set_implicit_use_of_stdout()
        if self.get_operand_list_length() == 0:
            self.set_implicit_use_of_stdin()
        else:
            self.all_operands_are_other_inputs()
