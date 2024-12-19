from graphgen.extractor.old.InputOutputInfo_generators.InputOutputInfoGenerator_Interface import \
    InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorAwk(InputOutputInfoGeneratorInterface):

    def generate_info(self) -> None:
        self.set_implicit_use_of_stdout()

        ## Does this set -f as configuration input?
        if self.does_flag_option_list_contain_at_least_one_of(["-f"]):
            if self.get_operand_list_length() == 0:
                self.set_implicit_use_of_stdin()
            else:
                self.all_operands_are_other_inputs()  # this is true also if empty
        else:
            if self.get_operand_list_length() == 1:
                self.set_implicit_use_of_stdin()
            else:
                self.all_but_first_operand_is_other_inputs()
