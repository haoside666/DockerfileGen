from graphgen.extractor.old.InputOutputInfo_generators.InputOutputInfoGenerator_Interface import \
    InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorRm(InputOutputInfoGeneratorInterface):
    # Which ones do affect input/output?
    # None
    def generate_info(self) -> None:
        self.all_operands_are_io()
