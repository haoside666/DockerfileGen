from typing import Tuple

from dockdepend.dependency.datatypes.DDType import DDType
from dockdepend.dependency.judgeor.Judge_Interface import JudgeInterface


# ENV Tuple
class JudgeEnvTuple(JudgeInterface):
    def get_dependence(self) -> Tuple[DDType, str]:
        return self.get_common_arg_dependence()
