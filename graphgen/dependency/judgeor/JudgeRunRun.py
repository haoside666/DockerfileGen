from graphgen.dependency.datatypes.DDType import DDType
from graphgen.dependency.judgeor.Judge_Interface import JudgeInterface
from graphgen.dockerfile_process.datatypes.ShellFeature import ShellFeature, instruct_feature_have_intersection
from graphgen.config.definitions import side_effect_command_set, UNKNOWN_PREFIX
from typing import Optional, Tuple, Set
from graphgen.config import global_config


# RUN RUN
class JudgeRunRun(JudgeInterface):
    def get_dependence(self) -> Tuple[DDType, str]:
        instruct_feat1: Optional[ShellFeature] = self.command_meta1.get_eigenvector()
        instruct_feat2: Optional[ShellFeature] = self.command_meta2.get_eigenvector()
        if instruct_feat1 is None or instruct_feat2 is None:
            return DDType.NONE, ""
        else:
            d_type, msg = instruct_feature_have_intersection(instruct_feat1, instruct_feat2)
            if d_type.value:
                return d_type, msg
            # 进行副作用影响依赖判断
            if not global_config.ignore_side_effect:
                side_effect_set1 = instruct_feat1.command_set & side_effect_command_set
                side_effect_set2 = instruct_feat2.command_set & side_effect_command_set
                if len(side_effect_set1) > 0:
                    return DDType.SIDE_EFFECT, f"Because previous instruction contain side effect command: {side_effect_set1}"
                elif side_effect_set2:
                    return DDType.SIDE_EFFECT, f"Because latter instruction contain side effect command: {side_effect_set2}"

            # 进行未识别命令依赖判断
            if not global_config.ignore_unknown_command:
                unknown_set1 = get_unknown_command_set(instruct_feat1.pkg_set)
                if unknown_set1:
                    return DDType.UNKNOWN_COMMAND, f"The previous instruction has unrecognized command: {unknown_set1}"
                else:
                    unknown_set2 = get_unknown_command_set(instruct_feat2.pkg_set)
                    if unknown_set2:
                        return DDType.UNKNOWN_COMMAND, f"The latter instruction has unrecognized command: {unknown_set2}"
            return DDType.NONE, ""


def get_unknown_command_set(command_set: Set[Tuple[str, str]]) -> set:
    return {x[0].replace(UNKNOWN_PREFIX, '') for x in command_set if x[0].startswith(UNKNOWN_PREFIX)}
