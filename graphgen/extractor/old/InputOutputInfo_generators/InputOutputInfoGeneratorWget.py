import os.path

from graphgen.extractor.old.InputOutputInfo_generators.InputOutputInfoGenerator_Interface import \
    InputOutputInfoGeneratorInterface
from graphgen.extractor.datatypes.BasicDatatypes import Option, WhichClassForArg
from graphgen.extractor import make_other_output


class InputOutputInfoGeneratorWget(InputOutputInfoGeneratorInterface):
    # Why wget can affect the generation of file stream information for subsequent commands?
    # example:
    #   wget -qO- https://github.com/powerivq/ttrss-pusher/releases/download/1.0.0/release-1.0.0.zip | unzip -
    #   curl -s https://api.github.com/repos/gentilkiwi/mimikatz/releases/latest \
    # 	| jq -r '.assets[].browser_download_url' \
    # 	| grep .'zip' \
    # 	| wget -i -

    def generate_info(self) -> None:
        operand_list = self.cmd_inv_after_io.operand_list
        # if not self.does_flag_option_list_contain_at_least_one_of(["-s"]):
        #     self.set_implicit_use_of_stdout()
        if len(operand_list) == 1:
            if not self.does_flag_option_list_contain_specific_parameter("-O"):
                operand = operand_list[0].get_name()
                operand = operand.rpartition("/")[-1]
                if self.does_flag_option_list_contain_specific_parameter("-P"):
                    option: Option = self.get_specific_option_by_specific_parameter("-P")
                    current_dir = option.get_arg()
                    operand_list[0].name = os.path.join(current_dir, operand)
                else:
                    operand_list[0].name = operand
                self.only_first_operand_is_other_output()
                self.pipe = operand
            else:
                option = self.get_specific_option_by_specific_parameter("-O")
                if option.option_arg == "-":
                    operand = operand_list[0].get_name()
                    operand = operand.rpartition("/")[-1]
                    self.pipe = operand
        elif len(operand_list) == 0:
            if self.does_flag_option_list_contain_specific_parameter("-O"):
                option = self.get_specific_option_by_specific_parameter("-O")
                operand = option.get_name()
                operand = operand.rpartition("/")[-1]
                self.pipe = operand
            else:
                if self.does_flag_option_list_contain_specific_parameter("-i"):
                    option = self.get_specific_option_by_specific_parameter("-i")
                    if option.option_arg == "-":
                        assert self.pipe != ""
                        self.add_one_element_to_operand_list(self.pipe, (WhichClassForArg.FILESTD, make_other_output()))
                    else:
                        # wget -i url.txt
                        # No certainty as to what files were downloaded
                        pass
                else:
                    pass
        else:
            if not self.does_flag_option_list_contain_specific_parameter("-O"):
                for index in range(len(operand_list)):
                    operand = operand_list[index].get_name()
                    if operand.startswith("https://") or operand.startswith("http://"):
                        operand = operand.rpartition("/")[-1]
                        self.add_one_element_to_operand_list(operand, (WhichClassForArg.FILESTD, make_other_output()))
            else:
                pass
