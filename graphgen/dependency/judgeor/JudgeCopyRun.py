from typing import Tuple

from graphgen.dependency.datatypes.DDType import DDType
from graphgen.dependency.judgeor.Judge_Interface import JudgeInterface


# COPY RUN
class JudgeCopyRun(JudgeInterface):
    def get_dependence(self) -> Tuple[DDType, str]:
        return self.get_add_or_copy_with_run_dependence()
