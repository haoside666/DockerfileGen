from typing import Tuple

from dockdepend.dependency.datatypes.DDType import DDType
from dockdepend.dependency.judgeor.Judge_Interface import JudgeInterface


# RUN Workdir
class JudgeRunWorkdir(JudgeInterface):
    def get_dependence(self) -> Tuple[DDType, str]:
        return self.get_run_with_dir_dependence()
