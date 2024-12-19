from typing import Tuple

from graphgen.dependency.datatypes.DDType import DDType
from graphgen.dependency.judgeor.Judge_Interface import JudgeInterface


# RUN Workdir
class JudgeRunWorkdir(JudgeInterface):
    def get_dependence(self) -> Tuple[DDType, str]:
        return self.get_run_with_dir_dependence()
