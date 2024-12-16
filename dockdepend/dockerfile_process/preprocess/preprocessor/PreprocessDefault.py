from dockdepend.dockerfile_process.preprocess.preprocessor.Preprocess_Interface import PreprocessInterface
from dockdepend.exception.CustomizedException import InstructFormatError


class PreprocessDefault(PreprocessInterface):
    def command_preprocess(self) -> None:
        if len(self.command.value) == 0:
            raise InstructFormatError("arg instruct format error")
        pass
