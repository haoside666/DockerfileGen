from graphgen.dockerfile_process.preprocess.preprocessor.Preprocess_Interface import PreprocessInterface


class PreprocessEntrypoint(PreprocessInterface):
    def command_preprocess(self) -> None:
        original_cmd = self.command.original.replace("ENTRYPOINT", "").strip()
        if original_cmd[0] == "[" and original_cmd[-1] == "]":
            types = "default"
        else:
            types = "shell"
        self.cmd_meta_init.get_operand().set_type(types)
