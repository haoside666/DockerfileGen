from dockdepend.extractor.feature_extract.FeatureInfo_generators.FeatureInfoGenerator_Interface import \
    FeatureInfoGeneratorInterface
from dockdepend.extractor.datatypes.AccessKindCommon import WhichClassForFeature, make_other_output, make_other_io
import os


class FeatureInfoGeneratorGit(FeatureInfoGeneratorInterface):
    def generate_info(self) -> None:
        if self.get_operand_list_length() > 0:
            command = self.get_first_operand_name_as_string()
            operand_list = self.cmd_inv_after_io.operand_list
            if command == "clone":
                if len(operand_list) == 2:
                    url = operand_list[1].get_name()
                    dir_name = extract_git_dir_name(url)
                    self.add_one_element_to_operand_list(dir_name, (WhichClassForFeature.FILESTD, make_other_output()))
                elif len(operand_list) == 3:
                    # url = operand_list[1].get_name()
                    # dir_name = extract_git_dir_name(url)
                    # real_dir = operand_list[2].get_name()
                    self.only_last_operand_is_other_output()
                    # self.add_one_element_to_operand_list(os.path.join(real_dir, dir_name),
                    #                                      (WhichClassForFeature.FILESTD, make_other_output()))
                else:
                    for index in range(len(operand_list)):
                        operand = operand_list[index].get_name()
                        if operand.startswith("https://") or operand.startswith("http://") or operand.startswith("git@"):
                            dir_name = extract_git_dir_name(operand)
                            self.add_one_element_to_operand_list(dir_name, (WhichClassForFeature.FILESTD, make_other_output()))
            else:
                length = len(operand_list)
                for index in range(length):
                    operand = operand_list[index].get_name()
                    if "/" in operand:
                        self.set_operand_element_by_index(index, (WhichClassForFeature.FILESTD, make_other_io()))
        self.add_one_element_to_operand_list("git", (WhichClassForFeature.PKG, None))


def extract_git_dir_name(url: str):
    name = os.path.basename(url)
    index = name.find(".git")
    if index != -1:
        return name[:index]
    else:
        t = name.rpartition(".")
        if t[0] == "":
            return name
        else:
            return t[0]
