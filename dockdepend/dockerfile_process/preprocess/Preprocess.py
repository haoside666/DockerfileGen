from .preprocessor.PreprocessAdd import PreprocessAdd
from .preprocessor.PreprocessArg import PreprocessArg
from .preprocessor.PreprocessCopy import PreprocessCopy
from .preprocessor.PreprocessDefault import PreprocessDefault
from .preprocessor.PreprocessEntrypoint import PreprocessEntrypoint
from .preprocessor.PreprocessEnv import PreprocessEnv
from .preprocessor.PreprocessHealthcheck import PreprocessHealthcheck
from .preprocessor.PreprocessRun import PreprocessRun
from .preprocessor.ProprocessCmd import PreprocessCmd
from dockerfile import Command
from .datatypes.InstructMetaInit import InstructMetaInit

DICT_CMD_NAME_TRANSFORMER_MODULE_MAPPER = {
    "RUN": PreprocessRun,
    'FROM': PreprocessDefault,
    'CMD': PreprocessCmd,
    'LABEL': PreprocessDefault,
    'MAINTAINER': PreprocessDefault,
    'EXPOSE': PreprocessDefault,
    'ENV': PreprocessEnv,
    'ADD': PreprocessAdd,
    'COPY': PreprocessCopy,
    'ENTRYPOINT': PreprocessEntrypoint,
    'VOLUME': PreprocessDefault,
    'USER': PreprocessDefault,
    'WORKDIR': PreprocessDefault,
    'ARG': PreprocessArg,
    'ONBUILD': PreprocessDefault,
    'STOPSIGNAL': PreprocessDefault,
    'HEALTHCHECK': PreprocessHealthcheck,
    'SHELL': PreprocessDefault
}


def preprocess(command: Command, build_ctx: str) -> InstructMetaInit:
    try:
        preprocess_class = DICT_CMD_NAME_TRANSFORMER_MODULE_MAPPER[command.cmd]
        # Initialize the preprocess object
        preprocess_object = preprocess_class(command, build_ctx)
        # preprocess
        preprocess_object.preprocess()
        return preprocess_object.get_command_meta()
    except Exception:
        raise
