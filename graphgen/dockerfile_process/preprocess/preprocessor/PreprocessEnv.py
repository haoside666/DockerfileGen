from graphgen.dockerfile_process.preprocess.preprocessor.Preprocess_Interface import PreprocessInterface
from graphgen.exception.CustomizedException import InstructFormatError
import re


class PreprocessEnv(PreprocessInterface):
    def command_preprocess(self) -> None:
        value = self.command.value
        if len(value) == 0:
            raise InstructFormatError("env instruct format error")
        length = len(value) // 2
        values = {}
        for i in range(length):
            key = value[2 * i]
            env_value = value[2 * i + 1].replace('"', '')
            env_value = f'{env_value}'
            env_value = handle_special_variable_assignment_operation(env_value)
            values[key] = env_value
        self.cmd_meta_init.get_operand().set_value(values)


def handle_special_variable_assignment_operation(values):
    pattern = r"\$\{[a-zA-Z0-9_]+:[-+?=]([a-zA-Z0-9._]+)\}"
    if re.search(pattern, values):
        values = re.sub(pattern, lambda x: x.group(1), values)
    return values
