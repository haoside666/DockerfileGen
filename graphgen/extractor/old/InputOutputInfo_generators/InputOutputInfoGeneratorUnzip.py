from graphgen.extractor.old.InputOutputInfo_generators.InputOutputInfoGenerator_Interface import \
    InputOutputInfoGeneratorInterface
from graphgen.extractor.datatypes.BasicDatatypes import Option, Operand
from typing import Literal
import os.path


class InputOutputInfoGeneratorUnzip(InputOutputInfoGeneratorInterface):
    # Why would unzip be affected by the previous command and change the generation of streaming information?
    # example:
    #   For systems that support unzip for extracting files from standard input
    #   wget -qO- https://github.com/powerivq/ttrss-pusher/releases/download/1.0.0/release-1.0.0.zip | unzip -
    #   curl -sSL https://github.com/shadowsocksr/shadowsocksr-libev/archive/2.4.1.tar.gz | unzip -
    def generate_info(self) -> None:
        operand_list = self.cmd_inv_after_io.operand_list
        if len(operand_list) > 0:
            archive_name = operand_list[0].get_name()
            if archive_name == "-" and self.pipe != "":
                archive_name = self.pipe
            archive_name = extract_tar_filename(archive_name)
            current_dir = ""
            if self.does_flag_option_list_contain_specific_parameter("-d"):
                current_dir = self.get_option_arg_with_specific_parameter("-d")
                archive_name = os.path.join(current_dir, archive_name)

            if len(operand_list) > 1 and current_dir != "":
                for index in range(1, len(operand_list)):
                    operand = operand_list[index]
                    operand_arg = os.path.normpath(os.path.join(current_dir, operand.get_name()))
                    operand_list[index] = Operand(operand_arg)

            self.pipe = archive_name
            self.add_one_element_to_operand_list(archive_name)
            self.only_first_operand_is_other_input()
            self.all_but_first_operand_is_other_outputs()

    def get_option_arg_with_specific_parameter(self, parameter_name: Literal["-d"]) -> str:
        option: Option = self.get_specific_option_by_specific_parameter(parameter_name)
        option_arg = option.get_arg()
        return option_arg


def extract_tar_filename(archive_name: str):
    archive_name = os.path.basename(archive_name)
    index = archive_name.find(".zip")
    if index != -1:
        return archive_name[:index]
    else:
        t = archive_name.rpartition(".")
        if t[0] == "":
            return archive_name
        else:
            return t[0]
