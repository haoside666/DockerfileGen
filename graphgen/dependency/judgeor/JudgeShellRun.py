from typing import Tuple

from graphgen.dependency.datatypes.DDType import DDType
from graphgen.dependency.judgeor.Judge_Interface import JudgeInterface


# SHELL RUN
class JudgeShellRun(JudgeInterface):
    def get_dependence(self) -> Tuple[DDType, str]:
        if self.command_meta2.get_operand().type == "shell":
            return DDType.SHELL_RUN, "SHELL instruction dependency"
        else:
            return DDType.NONE, ""
