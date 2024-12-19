from graphgen.extractor.feature_extract.FeatureInfo_generators.FeatureInfoGenerator_Interface import \
    FeatureInfoGeneratorInterface
from graphgen.extractor.datatypes.AccessKindCommon import WhichClassForFeature, make_other_input


class FeatureInfoGeneratorPython(FeatureInfoGeneratorInterface):
    def generate_info(self) -> None:
        operand_list = self.cmd_inv_after_io.operand_list
        length = len(operand_list)
        if self.does_flag_option_list_contain_specific_parameter("-m"):
            index = self.get_index_by_flag_option_name("-m")
            option = self.cmd_inv_after_io.flag_option_list[index]
            if option.get_arg() == "pip" or option.get_arg() == "pip3":
                self.pip_generate_info()
        else:
            for index in range(length):
                operand = operand_list[index].get_name()
                if ".py" in operand or "/" in operand:
                    self.set_operand_element_by_index(index, (WhichClassForFeature.FILESTD, make_other_input()))
            self.add_one_element_to_operand_list("python", (WhichClassForFeature.PKG, None))

    def pip_generate_info(self):
        self.strip_startswith_is_hyphen_in_operand_list()
        operand_list = self.cmd_inv_after_io.operand_list
        if len(operand_list) > 0 and self.does_first_operand_contain(["install"]):
            if len(operand_list) == 1 and not self.does_flag_option_list_contain_at_least_one_of(["-e", "-r"]):
                self.add_one_element_to_operand_list("requirements.txt",
                                                     (WhichClassForFeature.FILESTD, make_other_input()))
            elif len(operand_list) == 2:
                operand_arg = operand_list[-1].get_name()
                if "/" in operand_arg or "." in operand_arg:
                    self.set_operand_element_by_index(1, (WhichClassForFeature.FILESTD, make_other_input()))
                else:
                    self.all_but_first_operand_is_pkg()
            else:
                self.all_but_first_operand_is_pkg()

        self.add_one_element_to_operand_list("pip", (WhichClassForFeature.PKG, None))
        self.add_one_element_to_operand_list("python", (WhichClassForFeature.PKG, None))
