import re
from dockdepend.dockerfile_process.preprocess.preprocessor.Preprocess_Interface import PreprocessInterface
from dockdepend.exception.CustomizedException import InstructFormatError

BASH_O_ARG = [
    "pipefail",
    "errexit",
    "errtrace",
    "noexec",
    "execfail",
    "allexport",
    "braceexpand",
    "emacs",
    "functrace",
    "hashall",
    "histexpand",
    "history",
    "ignoreeof",
    "keyword",
    "monitor",
    "noclobber",
    "noglob",
    "nolog",
    "notify",
    "nounset",
    "onecmd",
    "physical",
    "posix",
    "privileged",
    "verbose",
    "vi",
    "xtrace"
]


class PreprocessRun(PreprocessInterface):
    def is_bash_commmand(self, cmd):
        return re.search(r'/bin/.*?sh', cmd) != None

    def command_preprocess(self) -> None:
        original_cmd = self.command.original.replace("RUN", "").strip()
        if len(original_cmd) == 0:
            raise InstructFormatError("run instruct format error")
        operand = self.cmd_meta_init.get_operand()
        if original_cmd[0] == "[" and original_cmd[-1] == "]":
            types = "default"
            value = self.command.value
            cmd = value[0]
            pos = 0
            if cmd == "cmd":
                for i in range(1, len(value)):
                    if value[i] != "/S" and value[i] != "/C":
                        pos = i
                        break
            elif cmd == "powershell":
                for i in range(1, len(value)):
                    if value[i] != "-command":
                        pos = i
                        break
            elif self.is_bash_commmand(cmd):
                start = 1
                end = len(value)
                while start < end:
                    if value[start][0] == "-" or value[start] in BASH_O_ARG:
                        start = start + 1
                    else:
                        pos = start
                        break
            else:
                pos = 0
            subcmd = " ".join(list(value[0:pos]))
            values = " ".join(list(value[pos:]))
            operand.set_subcmd(subcmd)
        else:
            assert len(self.command.value) == 1
            types = "shell"
            values = str(self.command.value[0])

        # Processing command option format
        pattern = r'\s-[-]*[a-z][a-z-]*='
        if re.search(pattern, values):
            values = re.sub(pattern, lambda x: x.group()[:-1] + ' ', values)
        operand.set_type(types)
        operand.set_value(values)
