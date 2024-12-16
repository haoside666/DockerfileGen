from dockdepend.dockerfile_process.preprocess.preprocessor.Preprocess_Interface import PreprocessInterface
from dockdepend.exception.CustomizedException import InstructFormatError
import re


class PreprocessArg(PreprocessInterface):
    def command_preprocess(self) -> None:
        values = {}
        if len(self.command.value) == 0:
            raise InstructFormatError("arg instruct format error")
        for item in self.command.value:
            if "=" not in item:
                values[item] = ""
            else:
                key, value = item.split("=", maxsplit=1)
                values[key] = handle_special_variable_assignment_operation(value.replace('"', ''))
        self.cmd_meta_init.get_operand().set_value(values)


def handle_special_variable_assignment_operation(values):
    pattern = r"\$\{[a-zA-Z0-9_]+:[-+?=]([a-zA-Z0-9._]+)\}"
    if re.search(pattern, values):
        values = re.sub(pattern, lambda x: x.group(1), values)
    return values
