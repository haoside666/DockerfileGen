from dockdepend.extractor.old.InputOutputInfo_generators.InputOutputInfoGenerator_Interface import \
    InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorCat(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["-A", "-b", "-e", "-E", "--number", "-s", "t", "-T", "-u", "-v", "--help", "--version"]
    # list_of_all_options = []

    # Which ones do affect input/output?
    # basically only operands and the stdout as standard output (and stderr for errors)

    # Why cat can affect the generation of file stream information for subsequent commands?
    # example:
    #   cat ./vmware-ovftool.tar.* | tar -xzvf -
    def generate_info(self) -> None:
        self.set_implicit_use_of_stdout()
        self.if_no_operands_given_stdin_implicitly_used()
        self.all_operands_are_other_inputs()
        if self.get_operand_list_length() > 0:
            self.pipe = self.get_first_operand_name_as_string()
