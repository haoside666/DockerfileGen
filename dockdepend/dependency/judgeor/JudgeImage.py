from typing import Tuple

from dockdepend.dependency.datatypes.DDType import DDType
from dockdepend.dependency.judgeor.Judge_Interface import JudgeInterface


# ADD Dict
class JudgeImage(JudgeInterface):
    def get_dependence(self) -> Tuple[DDType, str]:
        return DDType.BASIC_IMAGE, "Image dependency"
