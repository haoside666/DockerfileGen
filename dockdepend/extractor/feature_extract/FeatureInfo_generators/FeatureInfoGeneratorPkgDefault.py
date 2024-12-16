from dockdepend.extractor.feature_extract.FeatureInfo_generators.FeatureInfoGenerator_Interface import \
    FeatureInfoGeneratorInterface
from dockdepend.extractor.datatypes.AccessKindCommon import WhichClassForFeature


class FeatureInfoGeneratorPkgDefault(FeatureInfoGeneratorInterface):
    def generate_info(self) -> None:
        if self.get_operand_list_length() > 0:
            if not self.does_first_operand_equal_arg("clean"):
                if self.does_first_operand_equal_arg("update"):
                    self.add_one_element_to_operand_list(self.cmd_inv_after_io.cmd_name,
                                                         (WhichClassForFeature.PKG, None))
                else:
                    self.all_but_first_operand_is_pkg()
                    if self.cmd_inv_after_io.does_operand_list_contain(["python-", "python3-"]):
                        self.add_one_element_to_operand_list("pip", (WhichClassForFeature.PKG, None))
                        self.add_one_element_to_operand_list("pip3", (WhichClassForFeature.PKG, None))
