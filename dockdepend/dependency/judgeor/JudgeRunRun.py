from dockdepend.dependency.datatypes.DDType import DDType
from dockdepend.dependency.judgeor.Judge_Interface import JudgeInterface
from dockdepend.dockerfile_process.datatypes.InsturctFeature import InstructFeature, instruct_feature_have_intersection
from dockdepend.config.definitions import side_effect_command_set
from typing import Optional, Tuple
from dockdepend.config import global_config


# RUN RUN
class JudgeRunRun(JudgeInterface):
    def get_dependence(self) -> Tuple[DDType, str]:
        instruct_feat1: Optional[InstructFeature] = self.command_meta1.get_eigenvector()
        instruct_feat2: Optional[InstructFeature] = self.command_meta2.get_eigenvector()
        if instruct_feat1 is None or instruct_feat2 is None:
            return DDType.NONE, ""
        else:
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
                unknown_set2 = get_unknown_command_set(instruct_feat2.pkg_set)
                if unknown_set1:
                    return DDType.UNKNOWN_COMMAND, f"The previous instruction has unrecognized command: {unknown_set1}"
                elif unknown_set2:
                    return DDType.UNKNOWN_COMMAND, f"The latter instruction has unrecognized command: {unknown_set2}"
            return instruct_feature_have_intersection(instruct_feat1, instruct_feat2)


def get_unknown_command_set(command_set: set) -> set:
    return {x.replace('unknown_', '') for x in command_set if x.startswith("unknown_")}
