from typing import Tuple

from graphgen.dependency.datatypes.DDType import DDType
from graphgen.dependency.judgeor.Judge_Interface import JudgeInterface


# VOLUME RUN
class JudgeVolumeRun(JudgeInterface):
    def get_dependence(self) -> Tuple[DDType, str]:
        return self.get_dir_list_with_run_dependence()
