from graphgen.dependency.datatypes.DDType import DDType
from graphgen.dependency.judgeor.Judge_Interface import JudgeInterface
from graphgen.dockerfile_process.datatypes.ShellFeature import ShellFeature
from typing import Optional, Tuple


# RUN USER
class JudgeRunUser(JudgeInterface):
    def get_dependence(self) -> Tuple[DDType, str]:
        instruct_feat: Optional[ShellFeature] = self.command_meta1.get_eigenvector()
        user1: str = self.command_meta1.get_attribute_user()
        user2: str = self.command_meta2.get_attribute_user()
        if instruct_feat is None:
            return DDType.NONE, ""
        elif user1 != user2:
            return DDType.RUN_USER1, "shell command user is different from the USER instruction"
        elif user2 in instruct_feat.user_set:
            return DDType.RUN_USER2, "the shell command contains the user in the USER instruction"
        else:
            return DDType.NONE, ""
