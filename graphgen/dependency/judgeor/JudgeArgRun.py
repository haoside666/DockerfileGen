from typing import Tuple

from graphgen.dependency.datatypes.DDType import DDType
from graphgen.dependency.judgeor.Judge_Interface import JudgeInterface


# ARG RUN
class JudgeArgRun(JudgeInterface):
    def get_dependence(self) -> Tuple[DDType, str]:
        dd_type, msg1 = self.get_common_arg_dependence()
        if dd_type.value:
            return dd_type, msg1
        else:
            dd_type, msg2 = self.get_special_env_with_run_dependence()
            if dd_type.value:
                return dd_type, msg2
            else:
                return dd_type, ""
