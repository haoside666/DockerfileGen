from typing import Tuple

from dockdepend.config import global_config
from dockdepend.dependency.datatypes.DDType import DDType
from dockdepend.dependency.judgeor.Judge_Interface import JudgeInterface


# User Workdir
class JudgeUserWorkdir(JudgeInterface):
    def get_dependence(self) -> Tuple[DDType, str]:
        # 进行一致性依赖判断
        if global_config.show_consistency_dependency:
            return DDType.CONSISTENCY, "consistency dependency"
        else:
            return DDType.NONE, ""
