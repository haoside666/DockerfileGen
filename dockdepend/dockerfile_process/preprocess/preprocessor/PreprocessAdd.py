import os.path

from dockdepend.dockerfile_process.preprocess.preprocessor.Preprocess_Interface import PreprocessInterface
from typing import Tuple, List


class PreprocessAdd(PreprocessInterface):
    def command_preprocess(self) -> None:
        try:
            self.path_segmentation_for_add_or_copy_instruct(self.command.value)
            command_type = self.get_type_by_command_original()
            if command_type == "default":
                self.get_add_or_copy_eigenvector_with_type_default()
            else:
                self.get_add_eigenvector_with_type_special()
        except Exception:
            raise

    def get_type_by_command_original(self) -> str:
        command_type = "default"
        original: str = self.command.original
        if self.match_url_or_git_repository(original):
            command_type = "special"
            self.cmd_meta_init.get_operand().set_type(command_type)
        return command_type

    # ADD git@git.example.com:foo/bar.git /bar
    # ADD https://raw.githubusercontent.com/sivel/speedtest-cli/master/speedtest.py /speedtest
    # ADD http://master.bioconductor.org/todays-date /tmp/
    def get_add_eigenvector_with_type_special(self):
        src_dir_pattern: Tuple = self.cmd_meta_init.get_operand().if_value_is_dir_dict_to_get_src_dir()
        path_list: List[str] = [os.path.basename(url).replace(".git", "") for url in src_dir_pattern]
        self.cmd_meta_init.set_eigenvector_init(path_list)
