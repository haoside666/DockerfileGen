from graphgen.dockerfile_process.preprocess.preprocessor.Preprocess_Interface import PreprocessInterface
from graphgen.exception.CustomizedException import InstructFormatError


class PreprocessHealthcheck(PreprocessInterface):
    def command_preprocess(self) -> None:
        value = self.command.value
        if len(value) == 0:
            raise InstructFormatError("healthcheck instruct format error")
        operand = self.cmd_meta_init.get_operand()
        if len(value) == 1:
            values = ()
        else:
            values = value[1:]
        sub_cmd = value[0]
        operand.set_value(values)
        operand.set_subcmd(sub_cmd)
