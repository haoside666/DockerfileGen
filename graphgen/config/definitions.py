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
URL_DOWNLOAD_COMMAND_SET = {"git", "curl", "wget"}
UNKNOWN_PREFIX = "unknown_"
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

PKG_DIRECTIVES = [
    'FROM',
    'RUN',
    'ENV',
    'ADD',
    'COPY',
    'USER',
    'WORKDIR',
    'SHELL'
]

CONFIG_DIRECTIVES = [
    'EXPOSE',
    'CMD',
    # 'ENTRYPOINT',
]

# PKG_CUT_DICT = {
#     "mvn": {'java'},
#     "npm": {'node'},
#     "pip": {'pip', 'python'},
#     "pip3": {'pip', 'python'},
#     "python": {'python', 'python3'},
#     "python3": {'python', 'python3'},
# }
LANGUAGE_SET = {
    "python", "python3", "java", "c++", "c", "c#", "javascript", "typescript", "ruby", "php", "swift", "kotlin", "go", "scala", "rust", "perl",
    "objective-c", "haskell", "erlang", "r", "matlab", "raku", "julia", "kotlin", "groovy", "dart", "lua", "racket",
    "clojure", "f#", "vb.net", "delphi", "vbscript", "tcl", "actionscript", "node",
}

TOOL_PKG_METHOD = {"git", "curl", "wget"}
PARSER_FLAG = True

# 系统包管理工具集合,不包括pip等语言包管理工具
SYSTEM_PACKAGE_TOOL_SET = {
    "apt", "apt-get", "apk", "aptitude", "yum", "dnf", "rpm", "zypper", "pacman", "homebrew", "portage", "slackpkg",
    "nix", "flatpak", "snap", "pkg", "pkgsrc"
}
