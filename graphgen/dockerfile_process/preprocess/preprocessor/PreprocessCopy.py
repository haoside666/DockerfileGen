import os.path
from graphgen.dockerfile_process.preprocess.preprocessor.Preprocess_Interface import PreprocessInterface
from typing import Tuple, List


class PreprocessCopy(PreprocessInterface):
    def command_preprocess(self) -> None:
        self.path_segmentation_for_add_or_copy_instruct(self.command.value)
        command_type = self.get_type_by_command_original()
        if command_type == "default":
            self.get_add_or_copy_eigenvector_with_type_default()
        else:
            self.get_copy_eigenvector_with_type_from()

    def get_type_by_command_original(self) -> str:
        command_type = "default"
        for args in self.command.flags:
            if "--from=" in args:
                command_type = "from"
                break
        if command_type == "from":
            self.cmd_meta_init.get_operand().set_type(command_type)
        # else:
        #     original: str = self.command.original
        #     if self.match_url_or_git_repository(original):
        #         command_type = "special"
        #         self.cmd_meta_init.get_operand().set_type(command_type)
        return command_type

    # COPY --from=build /usr/local/bin/kubectl /usr/local/bin/kubectl
    # COPY --from=builder /app/entrypoint.sh /
    # COPY --from=buildstage /usr/local/bin/ctb-* /usr/local/bin/
    # COPY --from=builder /1.txt /2.txt ./
    def get_copy_eigenvector_with_type_from(self):
        src_dir_pattern: Tuple = self.cmd_meta_init.get_operand().if_value_is_dir_dict_to_get_src_dir()
        path_list: List[str] = [os.path.basename(item[:-1]) if item[-1] == "/" else os.path.basename(item)
                                for item in src_dir_pattern]
        self.cmd_meta_init.set_eigenvector_init(path_list)
