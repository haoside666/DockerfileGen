from typing import Tuple

from dockdepend.dependency.datatypes.DDType import DDType
from dockdepend.dependency.judgeor.Judge_Interface import JudgeInterface


# ADD Dict
class JudgeNone(JudgeInterface):
    def get_dependence(self) -> Tuple[DDType, str]:
        return DDType.NONE, ""
