from typing import Tuple

from graphgen.dependency.datatypes.DDType import DDType
from graphgen.dependency.judgeor.Judge_Interface import JudgeInterface


# ARG Dict(ARG或ENV)
class JudgeArgDict(JudgeInterface):
    def get_dependence(self) -> Tuple[DDType, str]:
        return self.get_common_arg_dependence()
