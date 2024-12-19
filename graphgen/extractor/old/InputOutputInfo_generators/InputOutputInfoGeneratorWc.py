from graphgen.extractor.old.InputOutputInfo_generators.InputOutputInfoGenerator_Interface import \
    InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorWc(InputOutputInfoGeneratorInterface):
    def generate_info(self) -> None:
        if self.get_operand_list_length() == 0:
            self.set_implicit_use_of_stdin()
            self.set_implicit_use_of_stdout()
        else:
            self.all_operands_are_other_inputs()
            self.set_implicit_use_of_stdout()
