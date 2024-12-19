from typing import Set, List, Tuple

from dockdepend.dependency.datatypes.DDType import DDType
from dockdepend.util import standard_repr, standard_eq
from dockdepend.shell_parse.datatypes.PrimitiveFeature import PrimitiveFeature
from dockdepend.extractor.datatypes.CommandListFeature import CommandListFeature
from dockdepend.dockerfile_process.datatypes.DirectoryTree import DirectoryTree, trees_have_intersection


class ShellFeature:
    def __init__(self, p_feat: PrimitiveFeature, cmd_list_feature: CommandListFeature,
                 current_user: str) -> None:
        io_list, other_list = p_feat.split_other_list_to_two_part()
        if isinstance(p_feat.command, str):
            self.command = p_feat.command
        else:
            self.command = " | ".join(p_feat.command)
        assert len(cmd_list_feature.cmd_name_list) == 1
        self.command_set: Set = set(cmd_list_feature.cmd_name_list[0].split(','))
        self.pkg_set: Set = set([item.split("==")[0] for item in cmd_list_feature.pkg_list])
        self.other_set: Set = set(cmd_list_feature.other_list + other_list)
        self.user_set: Set = set(cmd_list_feature.user_list)
        self.var_p_set: Set = set(p_feat.var_p_list)
        self.var_c_set: Set = set(p_feat.var_c_list)
        input_list: List[str] = io_list + p_feat.redir_input_list + cmd_list_feature.input_list
        output_list: List[str] = io_list + p_feat.redir_output_list + cmd_list_feature.output_list

        self.input_path_tree: DirectoryTree = DirectoryTree(self.remove_wave_in_path(input_list, current_user))
        self.output_path_tree: DirectoryTree = DirectoryTree(self.remove_wave_in_path(output_list, current_user))

        # Remove the effect of subcommands
        # self.other_set.discard("$(command)")
        # self.other_set.discard('"$(command)"')

    def __repr__(self):
        return standard_repr(self)

    def __eq__(self, other):
        return standard_eq(self, other)

    def to_dict(self):
        json_data = dict()
        json_data["CommandSet"] = list(self.command_set)
        json_data["PkgSet"] = list(self.pkg_set)
        json_data["OtherSet"] = list(self.other_set)
        json_data["UserSet"] = list(self.user_set)
        json_data["VarPSet"] = list(self.var_p_set)
        json_data["VarCSet"] = list(self.var_c_set)
        json_data["InputTree"] = self.input_path_tree.to_dict()
        json_data["OutputTree"] = self.output_path_tree.to_dict()
        return json_data

    @staticmethod
    # Remove ~ from the path
    def remove_wave_in_path(path_list: List[str], current_user: str) -> List[str]:
        if current_user == "root":
            user_home = "/root"
        else:
            user_home = f"/home/{current_user}"

        return [item.replace("~", user_home) for item in path_list]


def instruct_feature_have_intersection(prior_feat: ShellFeature, latter_feat: ShellFeature) -> Tuple[DDType, str]:
    pkg_union_result = pkg_union(prior_feat.pkg_set, latter_feat.command_set)
    flag, common_path = io_union(prior_feat.output_path_tree, latter_feat.input_path_tree)
    var_union_result = var_union(prior_feat.var_p_set, latter_feat.var_c_set)
    other_union_result = other_union(prior_feat.other_set, latter_feat.other_set)
    if pkg_union_result:
        # print("have pkg intersection")
        return DDType.RUN_PKG, f"have shell pkg intersection,because exist intersection {pkg_union_result}"
    elif flag:
        # print("have io intersection")
        return DDType.RUN_IO, f"have shell io intersection,because common path {common_path}"
    elif var_union_result:
        # print("have var intersection")
        return DDType.RUN_VAR, f"have shell var intersection,because exist intersection {var_union_result}"
    elif other_union_result:
        # print("have other intersection")
        return DDType.RUN_OTHER, f"have shell other intersection,because exist intersection {other_union_result}"
    else:
        return DDType.NONE, ""


def pkg_union(prior_pkg_set: Set, latter_command_set: Set) -> Set:
    return prior_pkg_set & latter_command_set


def io_union(prior_output: DirectoryTree, latter_input: DirectoryTree) -> Tuple[bool, str]:
    return trees_have_intersection(prior_output, latter_input)


def var_union(prior_var_p: Set, latter_var_c: Set) -> Set:
    return prior_var_p & latter_var_c


def other_union(prior_other_set: Set, latter_other_set: Set) -> Set:
    return prior_other_set & latter_other_set
