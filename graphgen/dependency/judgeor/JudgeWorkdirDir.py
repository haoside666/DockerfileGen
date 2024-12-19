from typing import Tuple

from graphgen.dependency.datatypes.DDType import DDType
from graphgen.dependency.judgeor.Judge_Interface import JudgeInterface
from graphgen.dockerfile_process.datatypes.DirectoryTree import DirectoryTree, path_have_intersection_with_tree


# WORKDIR (ADD or COPY)
class JudgeWorkdirDir(JudgeInterface):
    def get_dependence(self) -> Tuple[DDType, str]:
        workdir_dir_list: Tuple[str] = self.command_meta1.get_operand().value
        search_tree: DirectoryTree = self.command_meta2.get_eigenvector()
        if search_tree is None:
            return DDType.NONE, ""
        for dir_path in workdir_dir_list:
            if path_have_intersection_with_tree(dir_path, search_tree):
                return DDType.FILE_DIR, "exist file or directory dependency"
        return DDType.NONE, ""
