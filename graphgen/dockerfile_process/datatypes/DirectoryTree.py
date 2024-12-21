import os.path
from pathlib import Path
from typing import List, Dict, Tuple, Set
from graphgen.util import standard_repr, standard_eq


class DirectoryTree:
    def __init__(self, path_list: List[str]) -> None:
        self.root: Dict = self.build_tree(path_list)

    def __repr__(self):
        return standard_repr(self)

    def __eq__(self, other):
        return standard_eq(self, other)

    def to_dict(self):
        return self.root.__str__()

    def build_tree(self, path_list: List[str]) -> Dict:
        root = {}
        for path in path_list:
            directory_list = self.get_directory_list_by_parse_path(path)
            current_level = root
            for component in directory_list:
                if component not in current_level:
                    current_level[component] = {}
                current_level = current_level[component]
        return root

    @staticmethod
    def get_directory_list_by_parse_path(path: str):
        directory_list = list(Path(path).parts)
        return directory_list

    def is_empty(self):
        return len(self.root) == 0


def trees_have_intersection(prior_output_tree: DirectoryTree, latter_input_tree: DirectoryTree) -> Tuple[bool, str]:
    root1 = prior_output_tree.root
    root2 = latter_input_tree.root
    if not root1 or not root2:
        return False, ""

    flag, intersection_path = __have_intersection(root1, root2, [])
    if flag:
        return True, intersection_path
    else:
        return False, ""


def path_have_intersection_with_tree(src_path: str, search_tree: DirectoryTree) -> bool:
    directory_list = list(Path(src_path).parts)
    if search_tree is None:
        return False
    tree = search_tree.root
    for directory in directory_list:
        if directory not in tree:
            return False
        else:
            tree = tree[directory]
    return True


def __have_intersection(tree1, tree2, current_path: List[str]) -> Tuple[bool, str]:
    if not tree1 or not tree2:
        return True, os.path.join(*current_path)
    tree1_layer = set(tree1.keys())
    tree2_layer = set(tree2.keys())
    intersection_part = tree1_layer & tree2_layer
    if not intersection_part:
        return False, ""
    for item in intersection_part:
        current_path.append(item)
        flag, intersection_path = __have_intersection(tree1[item], tree2[item], current_path)
        if flag:
            return True, intersection_path
        else:
            current_path.pop()
    return False, ""


if __name__ == "__main__":
    dir_tree1 = DirectoryTree(
        ["/aaa/ddd/eee/fff", "/bbb", "/ccc"])
    print(dir_tree1.root)
    dir_tree2 = DirectoryTree(
        ["/aaa/ddd/eee/hhh", "/ddd", "/eee", "/bbb"])
    print(dir_tree2.root)
    print(trees_have_intersection(dir_tree1, dir_tree2))
    # src_path = "/aaa/bbb"
    # print(path_have_intersection_with_tree(src_path, dir_tree1))
