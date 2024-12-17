import os

ROOT_DIR = os.path.join(os.path.dirname(__file__), "../")
TEMP_CMD_PATH = os.path.abspath(os.path.join(ROOT_DIR, "./shell_parse", "temp_cmd"))

TEMP_VAR_C_LIST_PATH = os.path.abspath(os.path.join(ROOT_DIR, "./shell_parse", "temp_var"))
TEMP_B_TYPE_PATH = os.path.abspath(os.path.join(ROOT_DIR, "./shell_parse", "temp_b_type.json"))
# side_effect_command_set = {"gpg", "apt-key", "sh", "bash", "sudo"}
side_effect_command_set = {"sh", "bash", "sudo"}
PROGRAM_COMMAND_SET = {"python", "python3", "node", "java", "go", "php", "git", "curl", "wget", "make", "npm", "pip",
                       "pip3"}
DIR_COMMAND_SET = {"mkdir", "touch", "echo", "cat", "sed", "awk", "curl", "wget", "tar", "git"}
VALID_DIRECTIVES = [
    'FROM',
    'RUN',
    'CMD',
    'LABEL',
    'MAINTAINER',
    'EXPOSE',
    'ENV',
    'ADD',
    'COPY',
    'ENTRYPOINT',
    'VOLUME',
    'USER',
    'WORKDIR',
    'ARG',
    'ONBUILD',
    'STOPSIGNAL',
    'HEALTHCHECK',
    'SHELL'
]

NOT_CHANGE_DIRECTIVES = [
    'ARG',
    'ENV',
    'FROM',
    'CMD',
    'ENTRYPOINT',
    'LABEL',
    'MAINTAINER',
    'EXPOSE',
    'VOLUME',
    'ONBUILD',
    'STOPSIGNAL',
    'HEALTHCHECK',
    'SHELL'
]

IGNORE_DIRECTIVES = [
    'LABEL',
    'MAINTAINER',
    'ONBUILD',
    'STOPSIGNAL',
    'HEALTHCHECK',
]
