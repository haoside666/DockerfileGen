from dockerfile import Command
from dockdepend.util import standard_repr, standard_eq, return_empty_list_if_none_else_itself
from typing import List


class CommandList:
    def __init__(self, cmd_list: List[Command] = None) -> None:
        self.cmd_list: List[Command] = return_empty_list_if_none_else_itself(cmd_list)

    def __repr__(self):
        return standard_repr(self)

    def __eq__(self, other) -> bool:
        return standard_eq(self, other)

    def length(self) -> int:
        return len(self.cmd_list)

    def remove_redundant_command(self) -> None:
        new_command_list: List[Command] = []
        cmd_list = []
        entrypoint_list = []
        stopsignal_list = []
        healthcheck_list = []
        length = self.length()
        for index in range(length):
            if self.cmd_list[index].cmd == "CMD":
                cmd_list.append(index)
            elif self.cmd_list[index].cmd == "ENTRYPOINT":
                entrypoint_list.append(index)
            elif self.cmd_list[index].cmd == "STOPSIGNAL":
                stopsignal_list.append(index)
            elif self.cmd_list[index].cmd == "HEALTHCHECK":
                healthcheck_list.append(index)
        delete_cmd_list = self.get_delete_list(cmd_list)
        delete_entrypoint_list = self.get_delete_list(entrypoint_list)
        delete_stopsignal_list = self.get_delete_list(stopsignal_list)
        delete_healthcheck_list = self.get_delete_list(healthcheck_list)
        merge_delete_list = delete_cmd_list + delete_entrypoint_list + delete_stopsignal_list + delete_healthcheck_list
        for index in range(length):
            if index not in merge_delete_list:
                new_command_list.append(self.cmd_list[index])
        self.cmd_list = new_command_list

    @staticmethod
    def get_delete_list(lis):
        length = len(lis)
        if length < 2:
            return []
        else:
            return lis[0:length - 1]
