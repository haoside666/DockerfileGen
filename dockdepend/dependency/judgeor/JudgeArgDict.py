from typing import Tuple

from dockdepend.dependency.datatypes.DDType import DDType
from dockdepend.dependency.judgeor.Judge_Interface import JudgeInterface


# ARG Dict(ARG或ENV)
class JudgeArgDict(JudgeInterface):
    def get_dependence(self) -> Tuple[DDType, str]:
        return self.get_common_arg_dependence()
