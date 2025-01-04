from graphgen.extractor.feature_extract.FeatureInfo_generators.FeatureInfoGenerator_Interface import \
    FeatureInfoGeneratorInterface
from graphgen.extractor.datatypes.AccessKindCommon import WhichClassForFeature, make_other_input


class FeatureInfoGeneratorPip(FeatureInfoGeneratorInterface):
    def generate_info(self) -> None:
        self.strip_startswith_is_hyphen_in_operand_list()
        operand_list = self.cmd_inv_after_io.operand_list
        if len(operand_list) > 0:
            if self.does_first_operand_contain(["install"]):
                if len(operand_list) == 1 and not self.does_flag_option_list_contain_at_least_one_of(["-e", "-r"]):
                    self.add_one_element_to_operand_list("requirements.txt",
                                                         (WhichClassForFeature.FILESTD, make_other_input()))
                elif len(operand_list) == 2:
                    operand_arg = operand_list[-1].get_name()
                    if "==" not in operand_arg and ("/" in operand_arg or "." in operand_arg):
                        self.only_last_operand_is_io()
                    else:
                        self.all_but_first_operand_is_pkg()
                else:
                    self.all_but_first_operand_is_pkg()
                    operand_arg = operand_list[-1].get_name()
                    if "==" not in operand_arg and ("/" in operand_arg or "." in operand_arg):
                        self.only_last_operand_is_io()
            else:
                self.add_one_element_to_operand_list(".",
                                                     (WhichClassForFeature.FILESTD, make_other_input()))

        self.add_one_element_to_operand_list(self.cmd_inv_after_io.cmd_name, (WhichClassForFeature.PKG, None))
        self.add_one_element_to_operand_list("python", (WhichClassForFeature.PKG, None))
