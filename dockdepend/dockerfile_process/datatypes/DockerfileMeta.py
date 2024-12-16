import sys

from dockdepend.util import standard_repr, standard_eq
from typing import List
from dockerfile import Command
from dockdepend.config.definitions import VALID_DIRECTIVES
from .InstructMetaList import InstructMetaList
from dockdepend.dockerfile_process.preprocess.datatypes.InstructMetaPrefix import InstructMetaPrefix
from .CommandList import CommandList
from dockdepend.exception.CustomizedException import InstructNotFoundError


class DockerfileMeta:
    def __init__(self, parsed_dockerfile: List[Command]) -> None:
        self.stage_list: List[CommandList] = self.get_stage_list(parsed_dockerfile)
        self.is_mutil_stage: bool = (len(self.stage_list) > 1)
        self.stage_meta_prefix_list: List[List[InstructMetaPrefix]] = []
        self.stage_meta_list: List[InstructMetaList] = []

    def __repr__(self):
        return standard_repr(self)

    def __eq__(self, other) -> bool:
        return standard_eq(self, other)

    def add_element_to_stage_meta_init_list(self, cmd_meta_init_list: List[InstructMetaPrefix]) -> None:
        self.stage_meta_prefix_list.append(cmd_meta_init_list)

    def add_element_to_stage_meta_list(self, cmd_meta_list: InstructMetaList) -> None:
        self.stage_meta_list.append(cmd_meta_list)

    @staticmethod
    def get_stage_list(parsed_dockerfile: List[Command]) -> List[CommandList]:
        stage_list: List[CommandList] = []
        cut_pos: List[int] = []
        try:
            length = len(parsed_dockerfile)
            for index in range(length):
                # Check directives
                command = parsed_dockerfile[index]
                if command.cmd not in VALID_DIRECTIVES:
                    # Not valid dockerfile
                    raise InstructNotFoundError('found invalid directive {}'.format(command.cmd))
                if command.cmd == "FROM":
                    cut_pos.append(index)
            cut_pos.append(length)
            # TODO: In order to solve the situation of ARG from FROM
            cut_pos[0] = 0
            for i in range(len(cut_pos) - 1):
                start = cut_pos[i]
                end = cut_pos[i + 1]
                command_list = CommandList(parsed_dockerfile[start:end])
                command_list.remove_redundant_command()
                stage_list.append(command_list)
            return stage_list
        except Exception as ex:
            print("ERROR: dockerfile parse is abnormal:{}\n".format(ex.args[0]), file=sys.stderr)
            raise
