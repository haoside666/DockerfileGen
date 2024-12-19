from graphgen.extractor.feature_extract.FeatureInfo_generators.FeatureInfoGenerator_Interface import \
    FeatureInfoGeneratorInterface
from graphgen.extractor.datatypes.AccessKindCommon import get_access_from_string, WhichClassForFeature
from graphgen.extractor.datatypes.BasicDatatypes import Option, Operand
from typing import Literal
import os.path


class FeatureInfoGeneratorTar(FeatureInfoGeneratorInterface):
    # -c (Create):
    # tar -cvf archive.tar files: Creates a new tar archive, -f is followed by the specified archive name.
    # -t (List):
    # tar -tvf archive.tar: Lists the contents of a tar archive.
    # -r (Append):
    # tar -rvf archive.tar newfile: Appends files to an existing tar archive.
    # -x (Extract):
    # tar -xvf archive.tar: Extracts files from a tar archive.
    # -u (Update):
    # tar -uvf archive.tar updated_file: Updates the tar archive, adding only new or modified files.
    #
    # Why would tar be affected by the previous command and change the generation of streaming information?
    # example:
    #   curl -s ftp://ftp.ncbi.nlm.nih.gov/entrez/entrezdirect/edirect.tar.gz | tar xzf -

    def generate_info(self) -> None:
        if self.does_flag_option_list_contain_specific_parameter("-f"):
            operand_list = self.cmd_inv_after_io.operand_list
            if self.does_flag_option_list_contain_at_least_one_of(["-c", "-r", "-u"]):
                assert (len(operand_list) >= 1)
                self.set_kind_to_specific_parameter("-f", "CONFIG_OUTPUT")
                self.set_c_mode(operand_list)
            elif self.does_flag_option_list_contain_specific_parameter("-t"):
                assert (len(operand_list) == 0)
                self.set_kind_to_specific_parameter("-f", "CONFIG_INPUT")
            elif self.does_flag_option_list_contain_specific_parameter("-x"):
                self.set_kind_to_specific_parameter("-f", "CONFIG_INPUT")
                archive_name = self.get_option_arg_with_specific_parameter("-f")
                if archive_name == "-" and self.pipe != "":
                    archive_name = self.pipe
                self.set_x_mode(archive_name)
        else:
            if self.does_flag_option_list_contain_specific_parameter("-x"):
                archive_name = self.pipe
                self.set_x_mode(archive_name)

    def set_c_mode(self, operand_list):
        if self.does_flag_option_list_contain_specific_parameter("-C"):
            self.set_kind_to_specific_parameter("-C", "CONFIG_INPUT")
            current_dir = self.get_option_arg_with_specific_parameter("-C")
            for index in range(len(operand_list)):
                operand = operand_list[index]
                operand_arg = os.path.normpath(os.path.join(current_dir, operand.get_name()))
                operand_list[index] = Operand(operand_arg)
        self.all_operands_are_other_input()

    def set_x_mode(self, archive_name):
        current_dir = ""
        if self.does_flag_option_list_contain_specific_parameter("-C"):
            self.set_kind_to_specific_parameter("-C", "CONFIG_OUTPUT")
            current_dir = self.get_option_arg_with_specific_parameter("-C")
            operand_arg = os.path.join(current_dir, extract_tar_filename(archive_name))
        else:
            operand_arg = extract_tar_filename(archive_name)
        operand_list = self.cmd_inv_after_io.operand_list
        if len(operand_list) != 0 and current_dir != "":
            for index in range(len(operand_list)):
                operand2 = operand_list[index]
                operand_arg2 = os.path.normpath(os.path.join(current_dir, operand2.get_name()))
                operand_list[index] = Operand(operand_arg2)

        self.pipe = operand_arg
        self.add_one_element_to_operand_list(operand_arg, (WhichClassForFeature.ARGSTRING, None))
        self.all_operands_are_other_output()

    def get_option_arg_with_specific_parameter(self, parameter_name: Literal["-C", "-f"]) -> str:
        option: Option = self.get_specific_option_by_specific_parameter(parameter_name)
        option_arg = option.get_arg()
        return option_arg

    def set_kind_to_specific_parameter(self, parameter_name: Literal["-C", "-f"], kind: str) -> None:
        index = self.get_index_by_flag_option_name(parameter_name)
        self.reset_flagoption_list_by_index(index, get_access_from_string(kind))


def extract_tar_filename(archive_name: str):
    archive_name = os.path.basename(archive_name)
    index = archive_name.find(".tar")
    if index != -1:
        return archive_name[:index]
    else:
        t = archive_name.rpartition(".")
        if t[0] == "":
            return archive_name
        else:
            return t[0]
