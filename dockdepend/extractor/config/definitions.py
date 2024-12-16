### which argument strings in command_flag_option_info/data/*.json files are interpreted as filenames/directories
INDICATORS_FOR_FILENAMES = ["FILE", "DIR"]

special_command_list_in_parse = ["ln", "curl", "tar", "wget", "sed", "useradd", "adduser", "git"]
# side_effectful_command_set = {"gpg", "apt-key", "sh", "bash", "sudo"}
UNKNOWN_DIR_COMMAND_SET = {"lein", "julia", "pipenv"}
# View and set simple information commands, often without regard for their dependencies
IGNORE_COMMAND_SET = {"set", "strip", "lsb_release", "[", "find", "sha256sum"}
